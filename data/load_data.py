from json import loads

from data.database import Database
from data.secondary_data_io import load
from lib.options import SCORING_METHODS
from lib.conversion import sparse, deserialize, deep_deserialize, deserialize_and_hashablize

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

    return [(deserialize(word, ignore_syllables), score) for (word, score) in results]
# plyint: enable=too-many-arguments

def load_chains(weighting, unstressed, ignore_syllables):
    loader = _load_phonemes if ignore_syllables else _load_syllables
    return loader(weighting, unstressed)

def load_distributions(weighting, ignore_syllables):
    distribution = 'word_length' if ignore_syllables else 'stress_pattern'
    return load('{}_distributions'.format(distribution))[weighting]

def _load_phonemes(weighting, unstressed):
    sql = "select word_length, word_position, phoneme, next_phonemes_{} \
        from phonemes where unstressed = {};".format(weighting, unstressed)
    results = Database.fetch(sql)

    output = []
    for word_length, word_position, phoneme, next_phonemes in results:
        sparse(output, word_length, [])
        sparse(output[word_length], word_position, {})

        output[word_length][word_position][phoneme] = loads(next_phonemes)

    return output

def _load_syllables(weighting, unstressed):
    stressing = ' = ' if unstressed else ' != '
    sql = "select word_length, word_position, stress, next_stress, syllable, \
        next_syllables_{} from syllables where stress{}'ignore_stress';"\
        .format(weighting, stressing)
    results = Database.fetch(sql)

    output = []
    for length, position, stressing, next_stressing, syllable, next_syllables in results:
        syllable = deserialize_and_hashablize(syllable)
        next_syllables = deep_deserialize(next_syllables)

        sparse(output, length, [])
        sparse(output[length], position, {})
        output[length][position].setdefault(stressing, {}).setdefault(next_stressing, {})\
            .setdefault(syllable, {})

        output[length][position][stressing][next_stressing][syllable] = next_syllables

    return output
