import sys

from data.parse.primary import frequency_list
from data.parse.primary.pronouncing_dictionary import PronouncingDictionary
from data.parse.secondary.absolute_chain import AbsoluteChain
from data.parse.secondary.most_probable_words import MostProbableWords
from data.database import Database
from data.schema import Schema
from lib.options import booleans_to_strings

class DatabaseInitializer():
    def __init__(self):
        self.schema = Schema(Database())
        self.schema.schema()

    def initialize_words(self):
        word_frequencies = frequency_list.parse()
        words, self.phoneme_chains, word_length_distributions = \
            PronouncingDictionary(word_frequencies).parse()
        self.schema.words(words)
        self.schema.word_length_distributions(word_length_distributions)

    def initialize_phoneme_chains(self):
        self.word_lengths = {'weighted': {}, 'unweighted': {}}
        for unstressed in [False, True]:
            stressing = 'unstressed' if unstressed else 'stressed'

            self.word_lengths['weighted'][stressing] = \
              AbsoluteChain.parse(self.phoneme_chains['weighted'][stressing])
            self.word_lengths['unweighted'][stressing] = \
              AbsoluteChain.parse(self.phoneme_chains['unweighted'][stressing])

            self.schema.phonemes(
                self.word_lengths['weighted'][stressing],
                self.word_lengths['unweighted'][stressing],
                unstressed
            )

    def initialize_scores(self):
        for unstressed in [False, True]:
            for unweighted in [False, True]:
                for ignore_length in [False, True]:
                    for ignore_position in [False, True]:
                        for method_mean in [False, True]:
                            for method_addition in [False, True]:
                                self.save_scores(ignore_length,
                                                 ignore_position, 
                                                 unstressed,
                                                 unweighted, 
                                                 method_mean, 
                                                 method_addition)

    def save_scores(self, 
                    ignore_length,
                    ignore_position, 
                    unstressed, 
                    unweighted, 
                    method_mean, 
                    method_addition):
        options = ignore_position, unstressed, unweighted, method_mean, method_addition
        stressing, weighting = booleans_to_strings(unstressed, unweighted)
        word_scores = MostProbableWords(self.word_lengths[weighting][stressing],
                                        ignore_length,
                                        options)
        self.schema.scores(word_scores.get(), options)

    def finish(self):
        self.schema.finish()
        sys.stdout.write('Database successfully initialized.\n')

database_initializer = DatabaseInitializer()
database_initializer.initialize_words()
database_initializer.initialize_phoneme_chains()
database_initializer.initialize_scores()
database_initializer.finish()