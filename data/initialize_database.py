import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from parse.primary import frequency_list, pronouncing_dictionary
from parse.secondary.absolute_chain import AbsoluteChain
from parse.secondary.most_probable_words import MostProbableWords
from lib.options import booleans_to_strings
from database import Database
from schema import Schema

########### PHASE ZERO ####################

schema = Schema(Database())
schema.schema()

########### PHASE ONE ####################

word_frequencies = frequency_list.parse()
words, phoneme_chains = pronouncing_dictionary.parse(word_frequencies)
schema.words(words)

########### PHASE TWO ####################

most_probable_next_phonemes = {'weighted': {}, 'unweighted': {}}
for unstressed in [False, True]:
  stressing = 'unstressed' if unstressed else 'stressed'

  most_probable_next_phonemes['weighted'][stressing] = \
    AbsoluteChain.parse(phoneme_chains['weighted'][stressing])
  most_probable_next_phonemes['unweighted'][stressing] = \
    AbsoluteChain.parse(phoneme_chains['unweighted'][stressing])

  schema.phonemes(
      most_probable_next_phonemes['weighted'][stressing],
      most_probable_next_phonemes['unweighted'][stressing],
      unstressed
  )

########### PHASE THREE ####################

for unstressed in [False, True]:
  for unweighted in [False, True]:
    for method_mean in [False, True]:
      for method_addition in [False, True]:
        options = unstressed, unweighted, method_mean, method_addition
        stressing, weighting = booleans_to_strings(unstressed, unweighted)
        schema.scores(
            MostProbableWords.get(
                most_probable_next_phonemes[weighting][stressing],
                options
            ),
            options
        )

schema.finish()

sys.stdout.write('Database successfully initialized.\n')