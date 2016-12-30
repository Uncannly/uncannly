import random
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.present import Present
from lib.type_conversion import array_to_string
from lib.score import get_score
from lib.options import OPTION_VALUES, option_value_string_to_boolean, \
  option_value_boolean_to_string, MAX_WORD_LENGTH
from data.load_data import load_phonemes
from data.secondary_data_io import load_word_length_distribution

NEXT_PHONEMES_OPTIONS = {}
WORD_LENGTH_DISTRIBUTIONS = {}
for WEIGHTING in OPTION_VALUES['weighting']:
    for STRESSING in OPTION_VALUES['stressing']:
        UNSTRESSED = option_value_string_to_boolean(STRESSING)
        NEXT_PHONEMES_OPTIONS.setdefault(STRESSING, {}).setdefault(
            WEIGHTING, load_phonemes(WEIGHTING, UNSTRESSED)
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

        weighting = option_value_boolean_to_string('weighting', unweighted)

        word, phoneme, score, length = reset(ignore_length, weighting, min_length, max_length)

        count_fails = 0
        count_successes = 0
        words = []

        while True:
            phoneme, score = next_phoneme(phoneme=phoneme,
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
                 word_length,
                 score,
                 scoring_method,
                 score_threshold,
                 unweighted,
                 unstressed,
                 ignore_position,
                 length):

    stressing = option_value_boolean_to_string('stressing', unstressed)
    weighting = option_value_boolean_to_string('weighting', unweighted)

    position = 0 if ignore_position else word_length
    if position >= length:
        length = 0
    if len(NEXT_PHONEMES_OPTIONS[stressing][weighting][length]) == 0:
        length = 0
    if len(NEXT_PHONEMES_OPTIONS[stressing][weighting][length][position]) == 0:
        position = 0

    next_phonemes = NEXT_PHONEMES_OPTIONS[stressing][weighting][length][position]

    other_args = score, scoring_method, word_length, score_threshold
    return choose_next(next_phonemes[phoneme], test, other_args)
# pylint: enable=too-many-arguments,too-many-locals

def test(phoneme, probability, other_args):
    score, scoring_method, word_length, score_threshold = other_args
    score = get_score(score, scoring_method, probability, word_length)
    return (None, score) if score < score_threshold else (phoneme, score)

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
    thing_to_iterate_on = enumerate(WORD_LENGTH_DISTRIBUTIONS[weighting][1:])
    other_args = min_length, max_length
    length = None
    while length is None:
        length = choose_next(thing_to_iterate_on, bind_length, other_args)
    return length

def bind_length(length, _, other_args):
    min_length, max_length = other_args
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

def choose_next(thing_to_iterate_on, method, other_args):
    random_number = random.random()
    accumulated_probability = 0
    for other_thing, probability in thing_to_iterate_on:
        accumulated_probability += probability
        if accumulated_probability > random_number:
            return method(other_thing, probability, other_args)