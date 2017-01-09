import sys
import random

from data.secondary_data_io import load
from data.load_data import load_syllables
from lib.present import for_web_syllables
from lib.conversion import to_sig_figs
from lib.score import get_score
from lib.cumulative_distribution import choose_next
from lib.options import option_value_boolean_to_string

# pylint: disable=too-few-public-methods,too-many-locals
class RandomModeSyllables(object):
    def __init__(self, options):
        self.interface = options['interface']
        self.pool = options['pool']
        self.selection = options['selection']
        self.scoring_method = options['scoring_method']
        self.score_threshold = options['score_threshold']
        self.unweighted = options['unweighted']
        self.unstressed = options['unstressed']
        self.exclude_real = options['exclude_real']
        self.ignore_position = options['ignore_position']
        self.ignore_length = options['ignore_length']
        self.min_length = options['min_length']
        self.max_length = options['max_length']

        self.weighting = option_value_boolean_to_string('weighting', self.unweighted)
        self.syllable_chains = load_syllables(self.weighting, self.unstressed)
        self.stress_pattern_distributions = load('stress_pattern_distributions')

        # self.selector = self.api_selector if self.interface == 'api' else self.cli_selector
        self.count_successes = 0
        self.count_fails = 0

        self.reset()

    def get(self):
        output = []
        count = 0

        while count < self.pool:
            syllable_length = len(self.stress_pattern)

            for i in range(0, syllable_length - 1):
                chosen_bucket = self.syllable_chains[syllable_length - 2]\
                   [i + 1][self.stress_pattern[i]][self.stress_pattern[i + 1]]

                if self.syllable is None:
                    syllable_bucket = chosen_bucket[tuple(['START_WORD'])]
                else:
                    syllable_bucket = chosen_bucket.get(self.syllable, None)

                if syllable_bucket is None:
                    # word = ['This shouldnt happen but we couldnt connect buckets']
                    self.word = []
                    break

                choose_next(syllable_bucket.iteritems(), self.test, syllable_length)

                if self.syllable is None:
                    break
                else:
                    self.word.append(self.syllable)

            final_word = str(self.word) + '\n'
            answer = for_web_syllables(self.word, self.exclude_real)
            if answer:
                output.append( (answer, to_sig_figs(self.score, 6)) )
                count += 1
            sys.stdout.write(final_word)
            self.reset()

        return output

    def reset(self):
        stress_pattern = choose_next(self.stress_pattern_distributions[self.weighting])
        self.stress_pattern = ['start_word'] + list(stress_pattern) + ['end_word']
        self.word = []
        self.syllable = None
        self.score = 1.0

    def test(self, syllable, probability, method_args):
        self.score = get_score(self.score, self.scoring_method, probability, method_args)
        self.syllable = None if self.score < self.score_threshold else syllable

# pylint: enable=too-few-public-methods,too-many-locals
