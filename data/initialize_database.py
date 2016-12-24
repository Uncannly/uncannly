import sys

from data.parse.primary import frequency_list
from data.parse.primary.pronouncing_dictionary import PronouncingDictionary
from data.parse.secondary.absolute_chain import AbsoluteChain
from data.parse.secondary.most_probable_words import MostProbableWords
from data.database import Database
from data.schema import Schema
from lib.options import booleans_to_strings

def initialize_database():

    ########### PHASE ZERO ####################

    schema = Schema(Database())
    schema.schema()

    ########### PHASE ONE ####################

    word_frequencies = frequency_list.parse()
    words, phoneme_chains = PronouncingDictionary(word_frequencies).parse()
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
                    word_scores = MostProbableWords(
                            most_probable_next_phonemes[weighting][stressing],
                            options
                    )
                    schema.scores(word_scores.get(), options)

    schema.finish()

    sys.stdout.write('Database successfully initialized.\n')

initialize_database()
