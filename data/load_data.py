import json
import ast

from data.database import Database
from data.secondary_data_io import load
from lib.options import SCORING_METHODS
from lib.conversion import sparse

def load_words():
    return Database.fetch("select * from words;")

# pylint: disable=too-many-arguments
def load_scores(scoring_method,
                ignore_length,
                ignore_position,
                unstressed,
                unweighted,
                ignore_syllables):
    method_mean, method_addition = SCORING_METHODS[scoring_method]
    length = ' = ' if ignore_length else ' != '
    sql = "select word, score from scores where length{}0 and \
        ignore_position = {} and unstressed = {} and unweighted = {} \
        and method_mean = {} and method_addition = {} and ignore_syllables = {};".format(
            length, ignore_position, unstressed, unweighted,
            method_mean, method_addition, ignore_syllables
        )

    results = Database.fetch(sql)
    if not ignore_syllables:
        results = [(ast.literal_eval(word), score) for (word, score) in results]
    return results
# plyint: enable=too-many-arguments

def load_chains(weighting, unstressed, ignore_syllables):
    loader = _load_phonemes if ignore_syllables else _load_syllables
    return loader(weighting, unstressed)

def load_distributions(weighting, ignore_syllables):
    if ignore_syllables:
        return load('word_length_distribution_{}'.format(weighting))
    else:
        return load('stress_pattern_distributions')[weighting]

def _load_phonemes(weighting, unstressed):
    sql = "select word_length, word_position, phoneme, next_phonemes_{} \
        from phonemes where unstressed = {};".format(weighting, unstressed)
    results = Database.fetch(sql)

    output = []
    for word_length, word_position, phoneme, next_phonemes in results:
        sparse(output, word_length, [])
        sparse(output[word_length], word_position, {})

        output[word_length][word_position][phoneme] = json.loads(next_phonemes)

    return output

def _load_syllables(weighting, unstressed):
    stressing = ' = ' if unstressed else ' != '
    sql = "select word_length, word_position, stressing, next_stressing, syllable, \
        next_syllables_{} from syllables where stressing{}'ignore_stress';"\
        .format(weighting, stressing)
    results = Database.fetch(sql)

    output = []
    for length, position, stressing, next_stressing, syllable, next_syllables in results:
        syllable = ast.literal_eval(syllable)
        next_syllables = ast.literal_eval(next_syllables)
        next_syllables = {ast.literal_eval(k): v for k, v in next_syllables.iteritems()}

        sparse(output, length, [])
        sparse(output[length], position, {})
        output[length][position].setdefault(stressing, {}).setdefault(next_stressing, {})\
            .setdefault(syllable, {})

        output[length][position][stressing][next_stressing][syllable] = next_syllables

    return output
