# from __future__ import print_function

from data.secondary_data_io import load
from lib.options import option_value_boolean_to_string
import random
import sys

# stress_pattern_distributions = load('normalized_stress_pattern_distributions')
# normalized_syllable_chains = load('normalized_syllable_chains')

# with open('explore_syllable_chains.txt', 'w') as filething:
#     print(syllable_chains['unweighted'][1], file=filething)

# with open('explore_normalized_syllable_chains.txt', 'w') as filething:
#     print(normalized_syllable_chains['unweighted'][1], file=filething)

# for _ in range(0, 50):
#     random_number = random.random()
#     accumulated_probability = 0
#     for potential_stress_pattern, probability in stress_pattern_distributions['weighted']:
#         accumulated_probability += probability
#         if accumulated_probability > random_number:
#             stress_pattern = potential_stress_pattern
#             break

#     stress_pattern = ['start_word'] + list(stress_pattern) + ['end_word']
#     syllable_length = len(stress_pattern)

#     word = ''
#     previous_syllable = None

#     for i in range(0, syllable_length - 1):
#         before_transition_stress = stress_pattern[i]
#         after_transition_stress = stress_pattern[i + 1]

#         chosen_bucket = normalized_syllable_chains['weighted'][syllable_length - 2][i + 1][before_transition_stress][after_transition_stress]

#         if previous_syllable is None:
#             previous_syllable_bucket = chosen_bucket[tuple(['START_WORD'])]
#         else:
#             previous_syllable_bucket = chosen_bucket.get(previous_syllable, None)

#         if previous_syllable_bucket is None:
#             word = ['This shouldnt happen but we couldnt connect buckets']
#             break

#         random_number = random.random()
#         accumulated_probability = 0
#         for potential_next_syllable, probability in previous_syllable_bucket.iteritems():
#             accumulated_probability += probability
#             if accumulated_probability > random_number:
#                 next_syllable = potential_next_syllable
#                 break

#         word += str(next_syllable)
#         previous_syllable = next_syllable

#     sys.stdout.write(''.join(word) + '\n')

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

        weighting = option_value_boolean_to_string('weighting', self.unweighted)
        # self.syllable_chains = load_phonemes(weighting, self.unstressed)
        self.stress_pattern_distributions = load('stress_pattern_distributions')

        # self.selector = self.api_selector if self.interface == 'api' else self.cli_selector
        self.count_successes = 0
        self.count_fails = 0

        # self.reset()

    def get(self):
        message = 'Not yet implemented. Please ignore syllables.'
        sys.stdout.write(message + '\n')
        return [(message, 0)]