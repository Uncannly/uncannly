import sys

from data.parse.primary import frequency_list
from data.parse.primary.pronouncing_dictionary import PronouncingDictionary
from data.parse.secondary import normalize
from data.parse.secondary.most_probable_words import MostProbableWords
from data.database import Database
from data.tables import Tables
from data.secondary_data_io import save
from lib.options import OPTION_VALUES, SCORING_METHODS, option_value_boolean_to_string

class DatabaseInitializer(object):
    def __init__(self):
        sys.stdout.write('Initializing database.\n\n')

        self.tables = Tables(Database())
        self.tables.schema()
        sys.stdout.write('Tables created.\n\n')

        self.phoneme_chains = None
        self.word_lengths = None
        self.syllable_chains = None

    def initialize_words(self):
        word_frequencies = frequency_list.parse()
        sys.stdout.write('Frequency list parsed.\n\n')

        words, self.phoneme_chains, self.word_length_distributions, \
            self.syllable_chains, self.stress_pattern_distributions = \
            PronouncingDictionary(word_frequencies).parse()
        sys.stdout.write('Pronouncing dictionary parsed into absolute chains and distributions.\n')

        self.tables.words(words)
        sys.stdout.write('Words table populated.\n\n')

    # pylint: disable=invalid-name
    def initialize_word_length_distributions(self):
        normalized_word_length_distributions = normalize.word_length_distributions(
            self.word_length_distributions)
        sys.stdout.write('Word length distributions normalized.\n')

        save(normalized_word_length_distributions, 'word_length_distributions')
        sys.stdout.write('Word length distributions saved.\n\n')

    def initialize_stress_pattern_distributions(self):
        normalized_stress_pattern_distributions = normalize.stress_pattern_distributions(
            self.stress_pattern_distributions)
        sys.stdout.write('Stress pattern distributions normalized.\n')

        save(normalized_stress_pattern_distributions, 'stress_pattern_distributions')
        sys.stdout.write('Stress pattern distributions saved.\n\n')
    # pylint: enable=invalid-name

    def initialize_syllable_chains(self):
        self.syllable_chains = normalize.syllable_chains(self.syllable_chains)
        sys.stdout.write('Syllable chains normalized.\n')

        self.tables.syllables(self.syllable_chains)
        sys.stdout.write('Syllable chain table populated.\n\n')

    def initialize_phoneme_chains(self):
        self.word_lengths = {'weighted': {}, 'unweighted': {}}
        for stressing in OPTION_VALUES['stressing']:
            self.word_lengths['weighted'][stressing] = \
                normalize.phoneme_chains(self.phoneme_chains['weighted'][stressing])
            self.word_lengths['unweighted'][stressing] = \
                normalize.phoneme_chains(self.phoneme_chains['unweighted'][stressing])
            sys.stdout.write('Phoneme chains {} normalized.\n'.format(stressing))

            self.tables.phonemes(
                self.word_lengths['weighted'][stressing],
                self.word_lengths['unweighted'][stressing],
                stressing
            )
        sys.stdout.write('Phoneme chain table populated.\n\n')

    # pylint: disable=too-many-locals,too-many-nested-blocks
    def initialize_scores(self):
        updated_limits = {}
        for stressing in OPTION_VALUES['stressing']:
            for weighting in OPTION_VALUES['weighting']:
                for length_consideration in OPTION_VALUES['length_consideration']:
                    for positioning in OPTION_VALUES['positioning']:
                        for method_mean in [False, True]:
                            for method_addition in [False, True]:
                                for ignore_syllables in [False, True]:
                                    scoring_method = SCORING_METHODS.keys()[
                                        SCORING_METHODS.values().index(
                                            (method_mean, method_addition)
                                        )
                                    ]
                                    options = positioning, stressing, weighting, \
                                        scoring_method, length_consideration, ignore_syllables

                                    source = self.word_lengths if ignore_syllables else \
                                        self.syllable_chains

                                    word_scores = MostProbableWords(source, options)

                                    scores, limit = word_scores.get()
                                    self.tables.scores(scores, options)

                                    syllable_use = option_value_boolean_to_string(
                                        'syllable_use', ignore_syllables)
                                    updated_limits\
                                        .setdefault(length_consideration, {})\
                                        .setdefault(positioning, {})\
                                        .setdefault(stressing, {})\
                                        .setdefault(weighting, {})\
                                        .setdefault(scoring_method, {})\
                                        .setdefault(syllable_use, limit)

        sys.stdout.write('Most probable words table populated.\n\n')

        save(updated_limits, 'default_limits')
        sys.stdout.write('Default limits per option combination updated.\n\n')
    # pylint: enable=too-many-locals,too-many-nested-blocks

    def finish(self):
        self.tables.finish()
        sys.stdout.write('Database successfully initialized!\n\n')

DATABASE_INITIALIZER = DatabaseInitializer()
DATABASE_INITIALIZER.initialize_words()
DATABASE_INITIALIZER.initialize_syllable_chains()
DATABASE_INITIALIZER.initialize_stress_pattern_distributions()
DATABASE_INITIALIZER.initialize_phoneme_chains()
DATABASE_INITIALIZER.initialize_word_length_distributions()
DATABASE_INITIALIZER.initialize_scores()
DATABASE_INITIALIZER.finish()
