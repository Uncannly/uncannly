import sys

from data.parse.primary import frequency_list
from data.parse.primary.pronouncing_dictionary import PronouncingDictionary
from data.parse.secondary import absolute_chain
from data.parse.secondary.most_probable_words import MostProbableWords
from data.database import Database
from data.tables import Tables
from data.secondary_data_io import save
from lib.options import OPTION_VALUES, SCORING_METHODS
from lib.conversion import snake_to_space

class DatabaseInitializer(object):
    def __init__(self):
        sys.stdout.write('Initializing database.\n\n')
        self.tables = Tables(Database())
        self.tables.schema()
        self.phoneme_chains = None
        self.word_lengths = None

    def initialize_words(self):
        word_frequencies = frequency_list.parse()
        sys.stdout.write('Frequency list parsed.\n\n')
        words, self.phoneme_chains, word_length_distributions, syllable_chains = \
            PronouncingDictionary(word_frequencies).parse()
        for weighting, distribution in word_length_distributions.iteritems():
            save(distribution, 'word_length_distribution_{}'.format(weighting))
        sys.stdout.write('Word length distributions saved.\n')
        self.tables.words(words)

        # this should become "initialize syllable chains"
        # because it does not have to do with words
        # and it should use self.syllable_chains like phonemes does above
        # and extract the normalization stuff from pronouncing dictionrary
        # into absolute chain or something akin to it
        self.tables.syllables(syllable_chains)

    def initialize_phoneme_chains(self):
        self.word_lengths = {'weighted': {}, 'unweighted': {}}
        for stressing in OPTION_VALUES['stressing']:
            self.word_lengths['weighted'][stressing] = \
              absolute_chain.parse(self.phoneme_chains['weighted'][stressing])
            self.word_lengths['unweighted'][stressing] = \
              absolute_chain.parse(self.phoneme_chains['unweighted'][stressing])
            sys.stdout.write('Phoneme chains {} normalized.\n'.format(stressing))

            self.tables.phonemes(
                self.word_lengths['weighted'][stressing],
                self.word_lengths['unweighted'][stressing],
                stressing
            )
        sys.stdout.write('Phoneme chain table populated.\n\n')

    def initialize_scores(self):
        updated_limits = {}
        for stressing in OPTION_VALUES['stressing']:
            for weighting in OPTION_VALUES['weighting']:
                for length_consideration in OPTION_VALUES['length_consideration']:
                    for positioning in OPTION_VALUES['positioning']:
                        for method_mean in [False, True]:
                            for method_addition in [False, True]:
                                scoring_method = SCORING_METHODS.keys()[
                                    SCORING_METHODS.values().index(
                                        (method_mean, method_addition)
                                    )
                                ]
                                options = positioning, stressing, weighting, scoring_method
                                word_scores = MostProbableWords(
                                    self.word_lengths,
                                    length_consideration,
                                    options)
                                scores, limit = word_scores.get()
                                self.tables.scores(scores, options)
                                updated_limits\
                                    .setdefault(length_consideration, {})\
                                    .setdefault(positioning, {})\
                                    .setdefault(stressing, {})\
                                    .setdefault(weighting, {})\
                                    .setdefault(scoring_method, limit)
                                sys.stdout.write('Most probable words {} {} {} {} {} done.\n'\
                                    .format(snake_to_space(stressing),
                                            snake_to_space(weighting),
                                            snake_to_space(length_consideration),
                                            snake_to_space(positioning),
                                            snake_to_space(scoring_method)))

        sys.stdout.write('Most probable words table populated.\n\n')
        save(updated_limits, 'default_limits')
        sys.stdout.write('Default limits per option combination updated.\n\n')

    def finish(self):
        self.tables.finish()
        sys.stdout.write('Database successfully initialized.\n\n')

DATABASE_INITIALIZER = DatabaseInitializer()
DATABASE_INITIALIZER.initialize_words()
DATABASE_INITIALIZER.initialize_phoneme_chains()
DATABASE_INITIALIZER.initialize_scores()
DATABASE_INITIALIZER.finish()
