import json

from data.database import Database
from lib.options import SCORING_METHODS

def load_words():
    return Database.fetch("select * from words;")

def load_scores(scoring_method, ignore_position, unstressed, unweighted):
    method_mean, method_addition = SCORING_METHODS[scoring_method]

    sql = "select word, score from scores where \
        ignore_position = {} and unstressed = {} and unweighted = {} \
        and method_mean = {} and method_addition = {};".format(
            ignore_position, unstressed, unweighted, method_mean, method_addition
        )

    return Database.fetch(sql)

def load_phonemes(unweighted, unstressed):
    next_phonemes = 'next_phonemes_unweighted' if unweighted else 'next_phonemes'
    sql = "select word_position, phoneme, {} from phonemes where unstressed = {};".format(
        next_phonemes, unstressed
    )
    results = Database.fetch(sql)

    output = [{}]
    for word_position, phoneme, next_phonemes in results:
        while word_position + 1 > len(output):
            output.append({})
        output[word_position][phoneme] = json.loads(next_phonemes)

    return output
