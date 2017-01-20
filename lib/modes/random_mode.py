import sys

from data.load_data import load_chains, load_distributions
from lib.select_and_present import select_for_web, select_and_maybe_present_for_terminal,\
    terminal_delayed_presentation
from lib.score import get_score
from lib.cumulative_distribution import choose_next
from lib.options import option_value_boolean_to_string, MAX_WORD_LENGTH, MAX_FAILS
from lib.ipa import clean_end_word_pseudovowel

# pylint: disable=too-few-public-methods
class RandomMode(object):
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
        self.ignore_syllables = options['ignore_syllables']
        self.min_length = options['min_length']
        self.max_length = options['max_length']

        weighting = option_value_boolean_to_string('weighting', self.unweighted)
        self.chains = load_chains(weighting, self.unstressed, self.ignore_syllables)
        self.distributions = load_distributions(weighting, self.ignore_syllables)

        self.selector = select_for_web if self.interface == 'api' else \
            select_and_maybe_present_for_terminal
        self.count_successes = 0
        self.count_fails = 0
        self.words = []

        self._reset()

    # pylint: disable=too-many-branches
    def get(self):
        while True:
            if self.ignore_syllables:
                current_position = len(self.word) + 1
                self._next_unit(current_position)

                if current_position > MAX_WORD_LENGTH:
                    self._reset()
                elif self.unit is None:
                    failure = self._maybe_fail()
                    if failure:
                        return failure
                elif self.unit == 'END_WORD':
                    if self.min_length is not None and current_position < self.min_length:
                        self._reset()
                    else:
                        success = self._maybe_succeed()
                        if success:
                            return success
                else:
                    if self.max_length is not None and current_position == self.max_length:
                        self.must_end = True

                    if self.max_length is not None and current_position > self.max_length:
                        self._reset()
                    else:
                        self.word.append(self.unit)

            else:
                for current_position in range(0, self.length - 1):
                    self._next_unit(current_position)

                    if self.unit is None or self.word is None:
                        break
                    else:
                        unit = clean_end_word_pseudovowel(self.unit)
                        if unit:
                            self.word.append(unit)

                if self.word:
                    success = self._maybe_succeed()
                    if success:
                        return success
                else:
                    failure = self._maybe_fail()
                    if failure:
                        return failure
                self._reset()
    # pylint: enable=too-many-branches

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

    def _next_unit(self, current_position):
        if self.ignore_syllables:
            position = 0 if self.ignore_position else current_position
            if position >= self.length or len(self.chains[self.length]) == 0:
                self.length = 0
            if len(self.chains[self.length][position]) == 0:
                position = 0

            next_units = self.chains[self.length][position]

            if self.must_end and 'END_WORD' in [x[0] for x in next_units[self.unit]]:
                self.unit = 'END_WORD'
            else:
                choose_next(next_units[self.unit], self._test, current_position)

        else:
            length = 0 if self.ignore_length else self.length - 2
            position = 0 if self.ignore_position else current_position + 1
            stress = self.stress_pattern[current_position]
            next_stress = self.stress_pattern[current_position + 1]
            chosen_bucket = self.chains[length][position][stress][next_stress]
            next_units = chosen_bucket.get(self.unit)

            if next_units is None:
                # this is because the syllable chosen, while it of course
                # exists in the first stress level, may not happen to exist
                # for the transition from that stress level to the next one
                # in the given stressing pattern
                self.word = None
            else:
                choose_next(next_units.iteritems(), self._test, current_position + 1)

    def _test(self, unit, probability, method_args):
        self.score = get_score(self.score, self.scoring_method, probability, method_args)
        self.unit = None if self.score < self.score_threshold else unit

    def _reset(self):
        if self.ignore_syllables:
            self.length = 0 if self.ignore_length else self._random_frame()
        else:
            self.stress_pattern = self._random_frame()
            self.stress_pattern = ['start_word'] + list(self.stress_pattern) + ['end_word']
            if self.unstressed:
                self.stress_pattern = ['ignore_stress' for _ in self.stress_pattern]
            self.length = len(self.stress_pattern)

        self.word = []
        self.unit = 'START_WORD' if self.ignore_syllables else tuple(['START_WORD'])
        self.score = 1.0
        self.must_end = False

    def _random_frame(self):
        frame = None
        while frame is None:
            distributions = enumerate(self.distributions[1:]) \
                if self.ignore_syllables else self.distributions
            frame = choose_next(distributions)
            length = frame if self.ignore_syllables else len(frame)
            if (self.min_length is not None and length < self.min_length) or \
                (self.max_length is not None and length > self.max_length):
                frame = None
        return frame

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
