import json

from data.database import Database
from lib.options import scoring_methods

def load_words():
  return Database.fetch("select * from words;")

def load_scores(scoring_method, unweighted, unstressed):
  method_mean, method_addition = scoring_methods[scoring_method]

  sql = "select word, score from scores where \
    unweighted = {} and unstressed = {} \
    and method_mean = {} and method_addition = {};".format(
        unweighted, unstressed, method_mean, method_addition
    )

  return Database.fetch(sql)

def load_phonemes(unweighted, unstressed):
  next_phonemes = 'next_phonemes_unweighted' if unweighted else 'next_phonemes'
  sql = "select phoneme, {} from phonemes where unstressed = {};".format(
      next_phonemes, unstressed
  )
  results = Database.fetch(sql)

  output = {}
  for phoneme, next_phonemes in results:
    output[phoneme] = json.loads(next_phonemes)

  return output
