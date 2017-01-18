import sys

from data.secondary_data_io import load
from data.load_data import load_phonemes
from lib.select_and_present import select_for_web, select_and_maybe_present_for_terminal,\
    terminal_delayed_presentation
from lib.score import get_score
from lib.cumulative_distribution import choose_next
from lib.options import option_value_boolean_to_string, MAX_WORD_LENGTH, MAX_FAILS
from lib.conversion import array_to_string


class RandomModePhonemes(object):
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
        self.ignore_syllables = True
        self.min_length = options['min_length']
        self.max_length = options['max_length']

        weighting = option_value_boolean_to_string('weighting', self.unweighted)
        self.phoneme_chains = load_phonemes(weighting, self.unstressed)
        self.word_length_distributions = load('word_length_distribution_{}'.format(weighting))

        self.selector = select_for_web if self.interface == 'api' else \
            select_and_maybe_present_for_terminal
        self.count_successes = 0
        self.count_fails = 0

        self._reset()

    def get(self):
        words = []

        while True:
            word_length = len(self.word) + 1
            self._next_phoneme(word_length)

            if word_length > MAX_WORD_LENGTH:
                self._reset()
            elif self.phoneme is None:
                failure = self._maybe_fail()
                if failure:
                    return failure
            elif self.phoneme == 'END_WORD':
                if self.min_length is not None and word_length < self.min_length:
                    self._reset()
                else:
                    success = self._maybe_succeed(words)
                    if success:
                        return success
            else:
                if self.max_length is not None and word_length == self.max_length:
                    self.must_end = True

                if self.max_length is not None and word_length > self.max_length:
                    self._reset()
                else:
                    self.word.append(self.phoneme)

    def _maybe_fail(self):
        self.count_fails += 1
        if self.count_fails > MAX_FAILS:
            return self._fail()
        self._reset()

    def _maybe_succeed(self, words):
        if self.interface == 'cli':
            self.word = array_to_string(self.word)
        selected_word = self.selector(self.word,
                                      self.score,
                                      self.unstressed,
                                      self.exclude_real,
                                      self.ignore_syllables,
                                      self.selection)
        if selected_word:
            words.append(selected_word)
            self.count_successes += 1
            if self.count_successes == self.pool:
                return self._succeed(words)
        self._reset()

    def _next_phoneme(self, word_length):
        position = 0 if self.ignore_position else word_length
        if position >= self.length:
            self.length = 0
        if len(self.phoneme_chains[self.length]) == 0:
            self.length = 0
        if len(self.phoneme_chains[self.length][position]) == 0:
            position = 0

        next_phonemes = self.phoneme_chains[self.length][position]

        if self.must_end and 'END_WORD' in [x[0] for x in next_phonemes[self.phoneme]]:
            self.phoneme = 'END_WORD'
        else:
            choose_next(next_phonemes[self.phoneme], self._test, word_length)

    def _test(self, phoneme, probability, method_args):
        self.score = get_score(self.score, self.scoring_method, probability, method_args)
        self.phoneme = None if self.score < self.score_threshold else phoneme

    def _reset(self):
        if self.ignore_length:
            length = 0
        else:
            length = self._random_length()
        self.word = []
        self.phoneme = 'START_WORD'
        self.score = 1.0
        self.length = length
        self.must_end = False

    def _random_length(self):
        # i mean, or we could slice the distributions and re-normalize.
        # that especially would make more sense once we end up implementing the
        # continuous re-evaluation style.
        length = None
        while length is None:
            distributions = enumerate(self.word_length_distributions[1:])
            length = choose_next(distributions)
            if (self.min_length is not None and length < self.min_length) or \
                (self.max_length is not None and length > self.max_length):
                length = None
        return length

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
