import sys

from data.secondary_data_io import load
from data.load_data import load_syllables
from lib.select_and_present import select_for_web, select_and_maybe_present_for_terminal,\
    terminal_delayed_presentation
from lib.score import get_score
from lib.cumulative_distribution import choose_next
from lib.options import option_value_boolean_to_string, MAX_FAILS
from lib.ipa import clean_end_word_pseudovowel

# pylint: disable=too-few-public-methods
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

        weighting = option_value_boolean_to_string('weighting', self.unweighted)
        self.syllable_chains = load_syllables(weighting, self.unstressed)
        self.stress_pattern_distributions = load('stress_pattern_distributions')[weighting]

        self.selector = select_for_web if self.interface == 'api' else \
            select_and_maybe_present_for_terminal
        self.count_successes = 0
        self.count_fails = 0
        self.words = []

        self._reset()

    def get(self):
        while True:
            for current_position in range(0, self.length - 1):
                self._next_syllable(current_position)

                if self.syllable is None:
                    break
                else:
                    syllable = clean_end_word_pseudovowel(self.syllable)
                    if syllable:
                        self.word.append(syllable)

            if self.word:
                success = self._maybe_succeed()
                if success:
                    return success
            else:
                failure = self._maybe_fail()
                if failure:
                    return failure
            self._reset()

    def _maybe_fail(self):
        self.count_fails += 1
        if self.count_fails > MAX_FAILS:
            return self._fail()
        self._reset()

    def _maybe_succeed(self):
        selected_word = self.selector(self.word,
                                      self.score,
                                      self.unstressed,
                                      self.exclude_real,
                                      self.ignore_syllables,
                                      self.selection)
        if selected_word:
            self.words.append(selected_word)
            self.count_successes += 1
            if self.count_successes == self.pool:
                return self._succeed()
        self._reset()

    def _next_syllable(self, current_position):
        length_bucket = 0 if self.ignore_length else self.length - 2
        position_bucket = 0 if self.ignore_position else current_position + 1
        stress_bucket = self.stress_pattern[current_position]
        next_stress_bucket = self.stress_pattern[current_position + 1]
        chosen_bucket = self.syllable_chains[length_bucket]\
           [position_bucket][stress_bucket][next_stress_bucket]
        syllable_bucket = chosen_bucket.get(self.syllable, None)

        if syllable_bucket is None:
            # this is because the syllable chosen, while it of course
            # exists in the first stress level, may not happen to exist
            # for the transition from that stress level to the next one
            # in the given stressing pattern
            self.word = None
        else:
            choose_next(syllable_bucket.iteritems(), self._test, current_position + 1)

    def _test(self, syllable, probability, method_args):
        self.score = get_score(self.score, self.scoring_method, probability, method_args)
        self.syllable = None if self.score < self.score_threshold else syllable

    def _reset(self):
        self.stress_pattern = self._random_stress_pattern()
        self.stress_pattern = ['start_word'] + list(self.stress_pattern) + ['end_word']
        if self.unstressed:
            self.stress_pattern = ['ignore_stress' for _ in self.stress_pattern]

        self.word = []
        self.syllable = tuple(['START_WORD'])
        self.score = 1.0
        self.length = len(self.stress_pattern)

    def _random_stress_pattern(self):
        stress_pattern = None
        while stress_pattern is None:
            stress_pattern = choose_next(self.stress_pattern_distributions)
            length = len(stress_pattern)
            if (self.min_length is not None and length < self.min_length) or \
                (self.max_length is not None and length > self.max_length):
                stress_pattern = None
        return stress_pattern

    def _fail(self):
        message = (
            '{} times consecutively failed to find a word above the score '
            'threshold. Please try lowering it.'
        ).format(MAX_FAILS)
        if self.interface == "cli":
            sys.stdout.write(message + '\n')
            return True
        return [tuple([message, None])]

    def _succeed(self):
        if self.selection:
            self.words.sort(key=lambda x: -x[1])
            self.words = self.words[:self.selection]
            if self.interface == 'cli':
                terminal_delayed_presentation(self.words)
                return True
        return self.words
# pylint: enable=too-few-public-methods
