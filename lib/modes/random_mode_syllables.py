import sys

from data.secondary_data_io import load
from data.load_data import load_syllables
from lib.select_and_present import select_for_web, select_and_maybe_present_for_terminal,\
    terminal_delayed_presentation
from lib.score import get_score
from lib.cumulative_distribution import choose_next
from lib.options import option_value_boolean_to_string, MAX_FAILS
from lib.ipa import clean_end_word_pseudovowel

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
        self.ignore_syllables = False
        self.min_length = options['min_length']
        self.max_length = options['max_length']

        self.weighting = option_value_boolean_to_string('weighting', self.unweighted)
        self.syllable_chains = load_syllables(self.weighting, self.unstressed)
        self.stress_pattern_distributions = load('stress_pattern_distributions')

        self.selector = select_for_web if self.interface == 'api' else \
            select_and_maybe_present_for_terminal
        self.count_successes = 0
        self.count_fails = 0

        self._reset()

    # pylint: disable=too-many-branches
    def get(self):
        words = []

        while self.count_successes < self.pool and self.count_fails < 1000:
            syllable_length = len(self.stress_pattern)
            length_bucket = 0 if self.ignore_length else syllable_length - 2

            for current_position in range(0, syllable_length - 1):
                position_bucket = 0 if self.ignore_position else current_position + 1
                chosen_bucket = self.syllable_chains[length_bucket]\
                   [position_bucket][self.stress_pattern[current_position]]\
                   [self.stress_pattern[current_position + 1]]

                if self.syllable is None:
                    syllable_bucket = chosen_bucket[tuple(['START_WORD'])]
                else:
                    syllable_bucket = chosen_bucket.get(self.syllable, None)

                if syllable_bucket is None:
                    # this is because the syllable chosen, while it of course
                    # exists in the first stress level, may not happen to exist
                    # for the transition from that stress level to the next one
                    # in the given stressing pattern
                    self.word = None
                    break

                choose_next(syllable_bucket.iteritems(), self._test, current_position + 1)

                if self.syllable is None:
                    break
                else:
                    syllable = clean_end_word_pseudovowel(self.syllable)
                    if syllable:
                        self.word.append(syllable)

            if self.word:
                result = self.selector(self.word,
                                       self.score,
                                       self.unstressed,
                                       self.exclude_real,
                                       self.ignore_syllables,
                                       self.selection)
                if result:
                    words.append(result)
                    self.count_successes += 1
                else:
                    self.count_fails += 1
            else:
                self.count_fails += 1
            self._reset()

        if self.count_fails >= 1000:
            return self._fail()
        else:
            return self._succeed(words)
    # pylint: enable=too-many-branches

    def _reset(self):
        stress_pattern = None
        while stress_pattern is None:
            stress_pattern = choose_next(self.stress_pattern_distributions[self.weighting])
            length = len(stress_pattern)
            if (self.min_length is not None and length < self.min_length) or \
                (self.max_length is not None and length > self.max_length):
                stress_pattern = None
        self.stress_pattern = ['start_word'] + list(stress_pattern) + ['end_word']
        if self.unstressed:
            self.stress_pattern = ['ignore_stress' for _ in self.stress_pattern]
        self.word = []
        self.syllable = None
        self.score = 1.0

    def _test(self, syllable, probability, method_args):
        self.score = get_score(self.score, self.scoring_method, probability, method_args)
        self.syllable = None if self.score < self.score_threshold else syllable

    def _fail(self):
        message = (
            '{} times consecutively failed to find a word above the score '
            'threshold. Please try lowering it.'
        ).format(MAX_FAILS)
        if self.interface == "cli":
            sys.stdout.write(message + '\n')
            return True
        return [tuple([message, None])]

    def _succeed(self, words):
        if self.selection:
            words.sort(key=lambda x: -x[1])
            words = words[:self.selection]
            if self.interface == 'cli':
                terminal_delayed_presentation(words)
                return True
        return words

# pylint: enable=too-few-public-methods,too-many-locals
