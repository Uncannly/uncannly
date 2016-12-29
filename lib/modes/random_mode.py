import random
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.present import Present
from lib.type_conversion import array_to_string
from lib.score import get_score
from lib.options import booleans_to_strings, MAX_WORD_LENGTH
from data.load_data import load_phonemes
from data.secondary_data_io import load_word_length_distribution

NEXT_PHONEMES_OPTIONS = {}
WORD_LENGTH_DISTRIBUTIONS = {}
for UNWEIGHTED in [False, True]:
    WEIGHTING = 'unweighted' if UNWEIGHTED else 'weighted'
    for UNSTRESSED in [False, True]:
        STRESSING = 'unstressed' if UNSTRESSED else 'stressed'
        NEXT_PHONEMES_OPTIONS.setdefault(STRESSING, {}).setdefault(
            WEIGHTING, load_phonemes(UNWEIGHTED, UNSTRESSED)
        )
    WORD_LENGTH_DISTRIBUTIONS[WEIGHTING] = load_word_length_distribution(WEIGHTING)

# pylint: disable=too-many-arguments,too-many-locals,too-many-branches
# pylint: disable=too-few-public-methods,too-many-nested-blocks
class RandomMode(object):
    @staticmethod
    def get(interface,
            pool,
            selection,
            scoring_method,
            score_threshold,
            unweighted,
            unstressed,
            exclude_real,
            ignore_position,
            ignore_length,
            min_length,
            max_length):

        selector = api_selector if interface == 'api' else cli_selector

        weighting = 'unweighted' if unweighted else 'weighted'

        word, phoneme, score, length = reset(ignore_length, weighting, min_length, max_length)

        count_fails = 0
        count_successes = 0
        words = []

        while True:
            phoneme, score = next_phoneme(phoneme=phoneme,
                                          random_number=random.random(),
                                          word_length=len(word) + 1,
                                          score=score,
                                          scoring_method=scoring_method,
                                          score_threshold=score_threshold,
                                          unweighted=unweighted,
                                          unstressed=unstressed,
                                          ignore_position=ignore_position,
                                          length=length)

            if phoneme is None:
                count_fails += 1
                if count_fails > 1000000:
                    return fail(interface)
                word, phoneme, score, length = reset(ignore_length,
                                                     weighting,
                                                     min_length,
                                                     max_length)
            else:
                if phoneme == 'END_WORD':
                    if min_length is not None and len(word) < min_length:
                        word, phoneme, score, length = reset(ignore_length,
                                                             weighting,
                                                             min_length,
                                                             max_length)
                    else:
                        selected_word = selector(word, selection, unstressed, exclude_real)
                        if selected_word:
                            words.append((selected_word, score))
                            count_successes += 1
                            if count_successes == pool:
                                return succeed(words, interface, selection)
                        word, phoneme, score, length = reset(ignore_length,
                                                             weighting,
                                                             min_length,
                                                             max_length)
                elif max_length is not None and len(word) >= max_length:
                    selected_word = selector(word, selection, unstressed, exclude_real)
                    if selected_word:
                        words.append((selected_word, score))
                        count_successes += 1
                        if count_successes == pool:
                            return succeed(words, interface, selection)
                    word, phoneme, score, length = reset(ignore_length,
                                                         weighting,
                                                         min_length,
                                                         max_length)
                elif len(word) > MAX_WORD_LENGTH:
                    word, phoneme, score, length = reset(ignore_length,
                                                         weighting,
                                                         min_length,
                                                         max_length)
                else:
                    word.append(phoneme)
# pylint: enable=too-many-arguments,too-many-locals,too-many-branches
# pylint: enable=too-few-public-methods,too-many-nested-blocks

# pylint: disable=too-many-arguments,too-many-locals
def next_phoneme(phoneme,
                 random_number,
                 word_length,
                 score,
                 scoring_method,
                 score_threshold,
                 unweighted,
                 unstressed,
                 ignore_position,
                 length):

    stressing, weighting = booleans_to_strings(unstressed, unweighted)

    position = 0 if ignore_position else word_length
    if position >= length:
        length = 0
    if len(NEXT_PHONEMES_OPTIONS[stressing][weighting][length]) == 0:
        length = 0
    if len(NEXT_PHONEMES_OPTIONS[stressing][weighting][length][position]) == 0:
        position = 0

    next_phonemes = NEXT_PHONEMES_OPTIONS[stressing][weighting][length][position]

    accumulated_probability = 0
    for (phoneme, probability) in next_phonemes[phoneme]:
        accumulated_probability += probability
        if accumulated_probability >= random_number:
            score = get_score(score, scoring_method, probability, word_length)
            return (None, score) if score < score_threshold else (phoneme, score)
# pylint: enable=too-many-arguments,too-many-locals

def cli_selector(word, selection, unstressed, exclude_real):
    stringified_word = array_to_string(word)
    return Present.for_terminal(word=stringified_word,
                                unstressed=unstressed,
                                exclude_real=exclude_real,
                                suppress_immediate=selection)

# pylint: disable=unused-argument
def api_selector(word, selection, unstressed, exclude_real):
    return Present.for_web(word, unstressed, exclude_real)
# pylint: enable=unused-argument

def reset(ignore_length, weighting, min_length, max_length):
    length = 0 if ignore_length else random_length(weighting, min_length, max_length)
    return ([], 'START_WORD', 1.0, length)

def random_length(weighting, min_length, max_length):
    # i mean, or we could slice the distributions and re-normalize.
    # that especially would make more sense once we end up implementing the
    # continuous re-evaluation style.
    while True:
        random_number = random.random()
        accumulated_probability = 0
        for length, probability in enumerate(WORD_LENGTH_DISTRIBUTIONS[weighting][1:]):
            accumulated_probability += probability
            if accumulated_probability >= random_number:
                if min_length is not None and length < min_length:
                    pass
                elif max_length is not None and length > max_length:
                    pass
                else:
                    return length

def fail(interface):
    message = (
        '1000000 times consecutively failed to find a word above the score '
        'threshold. Please try lowering it.'
    )
    return sys.stdout.write(message + '\n') if interface == "cli" else [message]

def succeed(words, interface, selection):
    if selection:
        words.sort(key=lambda x: -x[1])
        words = words[:selection]

    if interface == 'cli':
        if selection:
            for word, _ in words:
                sys.stdout.write(word + '\n')
    else:
        return [x[0] for x in words]
