import random
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.present import Present
from lib.type_conversion import array_to_string
from lib.score import get_score
from lib.options import OPTION_VALUES, option_value_string_to_boolean, \
  option_value_boolean_to_string, MAX_WORD_LENGTH
from data.load_data import load_phonemes
from data.secondary_data_io import load_word_length_distribution

# pylint: disable=too-many-arguments,too-many-locals,too-many-branches
# pylint: disable=too-few-public-methods,too-many-nested-blocks
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
        self.min_length = options['min_length']
        self.max_length = options['max_length']

        weighting = option_value_boolean_to_string('weighting', self.unweighted)
        self.next_phonemes_options = load_phonemes(weighting, self.unstressed)
        self.word_length_distributions = load_word_length_distribution(weighting)

        self.selector = self.api_selector if self.interface == 'api' else self.cli_selector
        self.count_successes = 0
        self.count_fails = 0

    def get(self):
        self.reset()
        words = []

        while True:
            word_length = len(self.word) + 1
            self.next_phoneme(word_length)

            if self.phoneme is None:
                failure = self.maybe_fail()
                if failure:
                    return failure
            elif self.phoneme == 'END_WORD':
                if self.min_length is not None and word_length < self.min_length:
                    self.reset()
                else:
                    success = self.maybe_succeed(words)
                    if success:
                        return success
            elif self.max_length is not None and word_length > self.max_length:
                success = self.maybe_succeed(words)
                if success:
                    return success
            elif word_length > MAX_WORD_LENGTH:
                self.reset()
            else:
                self.word.append(self.phoneme)
    # pylint: enable=too-many-arguments,too-many-locals,too-many-branches
    # pylint: enable=too-few-public-methods,too-many-nested-blocks

    def maybe_fail(self):
        self.count_fails += 1
        if self.count_fails > 1000000:
            return self.fail()
        self.reset()

    def maybe_succeed(self, words):
        selected_word = self.selector()
        if selected_word:
            words.append((selected_word, self.score))
            self.count_successes += 1
            if self.count_successes == self.pool:
                return self.succeed(words)
        self.reset()

    # pylint: disable=too-many-arguments,too-many-locals
    def next_phoneme(self, word_length):
        position = 0 if self.ignore_position else word_length
        if position >= self.length:
            self.length = 0
        if len(self.next_phonemes_options[self.length]) == 0:
            self.length = 0
        if len(self.next_phonemes_options[self.length][position]) == 0:
            position = 0

        next_phonemes = self.next_phonemes_options[self.length][position]

        choose_next(next_phonemes[self.phoneme], self.test, word_length)
    # pylint: enable=too-many-arguments,too-many-locals

    def test(self, phoneme, probability, word_length):
        self.score = get_score(self.score, self.scoring_method, probability, word_length)
        self.phoneme = None if self.score < self.score_threshold else phoneme

    def cli_selector(self):
        stringified_word = array_to_string(self.word)
        return Present.for_terminal(word=stringified_word,
                                    unstressed=self.unstressed,
                                    exclude_real=self.exclude_real,
                                    suppress_immediate=self.selection)

    def api_selector(self):
        return Present.for_web(self.word, self.unstressed, self.exclude_real)

    def reset(self):
        if self.ignore_length:
            length = 0
        else:
            length = self.random_length()
        self.word = []
        self.phoneme = 'START_WORD'
        self.score = 1.0
        self.length = length

    def random_length(self):
        # i mean, or we could slice the distributions and re-normalize.
        # that especially would make more sense once we end up implementing the
        # continuous re-evaluation style.
        length = None
        while length is None:
            distributions = enumerate(self.word_length_distributions[1:])
            length = choose_next(distributions, self.bind_length, None)
        return length

    def bind_length(self, length, _, __):
        if self.min_length is not None and length < self.min_length:
            pass
        elif self.max_length is not None and length > self.max_length:
            pass
        else:
            return length

    def fail(self):
        message = (
            '1000000 times consecutively failed to find a word above the score '
            'threshold. Please try lowering it.'
        )
        if self.interface == "cli":
            sys.stdout.write(message + '\n')
            return True
        else:
            return [message]

    def succeed(self, words):
        if self.selection:
            words.sort(key=lambda x: -x[1])
            words = words[:selection]

        if self.interface == 'cli':
            if self.selection:
                for word, _ in words:
                    sys.stdout.write(word + '\n')
            return True
        else:
            return [x[0] for x in words]

def choose_next(iterator, method, method_args):
    random_number = random.random()
    accumulated_probability = 0
    for item, probability in iterator:
        accumulated_probability += probability
        if accumulated_probability > random_number:
            return method(item, probability, method_args)
