import random
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.present import Present
from lib.type_conversion import array_to_string
from lib.score import get_score
from lib.options import booleans_to_strings
from data.load_data import load_phonemes

NEXT_PHONEMES_OPTIONS = {}
for UNSTRESSED in [False, True]:
    for UNWEIGHTED in [False, True]:
        STRESSING, WEIGHTING = booleans_to_strings(UNSTRESSED, UNWEIGHTED)
        NEXT_PHONEMES_OPTIONS.setdefault(STRESSING, {}).setdefault(
            WEIGHTING, load_phonemes(UNWEIGHTED, UNSTRESSED)
        )

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
            ignore_length):

        selector = api_selector if interface == 'api' else cli_selector

        word, phoneme, score, length = reset(ignore_length)

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
                word, phoneme, score, length = reset(ignore_length)
            else:
                if phoneme == 'END_WORD':
                    selected_word = selector(word, selection, unstressed, exclude_real)
                    if selected_word:
                        words.append((selected_word, score))
                        count_successes += 1
                        if count_successes == pool:
                            return succeed(words, interface, selection)
                    word, phoneme, score, length = reset(ignore_length)
                elif len(word) > 20:
                    word, phoneme, score, length = reset(ignore_length)
                else:
                    word.append(phoneme)

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

def cli_selector(word, selection, unstressed, exclude_real):
    stringified_word = array_to_string(word)
    return Present.for_terminal(word=stringified_word,
                                unstressed=unstressed,
                                exclude_real=exclude_real,
                                suppress_immediate=selection)

def api_selector(word, selection, unstressed, exclude_real):
    return Present.for_web(word, unstressed, exclude_real)

def reset(ignore_length):
    length = 0 if ignore_length else int(random.random() * 20)
    return ([], 'START_WORD', 1.0, length)

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
