import sys

from data.parse.primary import frequency_list
from data.parse.primary.pronouncing_dictionary import PronouncingDictionary
from data.parse.secondary import absolute_chain
from data.parse.secondary.most_probable_words import MostProbableWords
from data.database import Database
from data.tables import Tables
from data.secondary_data_io import save_word_length_distributions
from lib.options import OPTION_VALUES

class DatabaseInitializer(object):
    def __init__(self):
        self.tables = Tables(Database())
        self.tables.schema()
        self.phoneme_chains = None
        self.word_lengths = None

    def initialize_words(self):
        word_frequencies = frequency_list.parse()
        words, self.phoneme_chains, word_length_distributions = \
            PronouncingDictionary(word_frequencies).parse()
        self.tables.words(words)
        save_word_length_distributions(word_length_distributions)

    def initialize_phoneme_chains(self):
        self.word_lengths = {'weighted': {}, 'unweighted': {}}
        for stressing in OPTION_VALUES['stressing']:
            self.word_lengths['weighted'][stressing] = \
              absolute_chain.parse(self.phoneme_chains['weighted'][stressing])
            self.word_lengths['unweighted'][stressing] = \
              absolute_chain.parse(self.phoneme_chains['unweighted'][stressing])

            self.tables.phonemes(
                self.word_lengths['weighted'][stressing],
                self.word_lengths['unweighted'][stressing],
                stressing
            )

    def initialize_scores(self):
        for unstressed in [False, True]:
            for unweighted in [False, True]:
                for ignore_length in [False, True]:
                    for ignore_position in [False, True]:
                        for method_mean in [False, True]:
                            for method_addition in [False, True]:
                                options = ignore_position, unstressed, \
                                    unweighted, method_mean, method_addition
                                word_scores = MostProbableWords(
                                    self.word_lengths,
                                    ignore_length,
                                    options)
                                self.tables.scores(word_scores.get(), options)

    def finish(self):
        self.tables.finish()
        sys.stdout.write('Database successfully initialized.\n')

DATABASE_INITIALIZER = DatabaseInitializer()
DATABASE_INITIALIZER.initialize_words()
DATABASE_INITIALIZER.initialize_phoneme_chains()
DATABASE_INITIALIZER.initialize_scores()
DATABASE_INITIALIZER.finish()
