import sys
import random

from lib.select_and_present import select_for_web, select_and_maybe_present_for_terminal
from lib.options import TOO_FEW_MESSAGE, NO_WORDS_MESSAGE, POOL_DEFAULT
from data.load_data import load_scores

# pylint: disable=too-many-instance-attributes,too-few-public-methods
class TopMode(object):
    def __init__(self, options):
        self.interface = options.get('interface', 'api')
        self.pool = options.get('pool', POOL_DEFAULT)
        self.selection = options.get('selection')
        self.scoring_method = options.get('scoring_method')
        self.score_threshold = options.get('score_threshold')
        self.unweighted = options.get('unweighted')
        self.unstressed = options.get('unstressed')
        self.exclude_real = options.get('exclude_real')
        self.ignore_position = options.get('ignore_position')
        self.ignore_length = options.get('ignore_length')
        self.min_length = options.get('min_length')
        self.max_length = options.get('max_length')
        self.ignore_syllables = options.get('ignore_syllables')

    def get(self):
        most_probable_words = load_scores(self.scoring_method,
                                          self.ignore_length,
                                          self.ignore_position,
                                          self.unstressed,
                                          self.unweighted,
                                          self.ignore_syllables)
        most_probable_words.sort(key=lambda x: -x[1])
        most_probable_words = most_probable_words[0:int(self.pool)]

        if self.selection:
            selector = api_select_random if self.interface == 'api' else cli_select_random
        else:
            self.selection = self.pool
            selector = api_select_top if self.interface == 'api' else cli_select_top

        words = []
        for word, score in most_probable_words:
            length = len(word)

            if score < self.score_threshold:
                break
            elif self.min_length is not None and length < self.min_length:
                pass
            elif self.max_length is not None and length > self.max_length:
                pass
            elif (word, score) in words:
                pass
            else:
                words.append((word, score))

        return selector(words,
                        self.selection,
                        self.unstressed,
                        self.exclude_real,
                        self.ignore_syllables)
# pylint: enable=too-many-instance-attributes,too-few-public-methods

def cli_select_top(words, selection, unstressed, exclude_real, ignore_syllables):
    if len(words) > 0:
        i = 0
        for _ in xrange(selection):
            presented = None
            while not presented:
                if i == len(words):
                    return sys.stdout.write(TOO_FEW_MESSAGE)

                word, score = words[i]
                presented = select_and_maybe_present_for_terminal(
                    word, score, unstressed, exclude_real, ignore_syllables,
                    suppress_immediate_presentation=False)

                i += 1
    else:
        sys.stdout.write(NO_WORDS_MESSAGE)

def cli_select_random(words, selection, unstressed, exclude_real, ignore_syllables):
    if len(words) > 0:
        for _ in xrange(selection):
            presented = None
            while not presented:
                word, score = random.choice(words)
                presented = select_and_maybe_present_for_terminal(
                    word, score, unstressed, exclude_real, ignore_syllables,
                    suppress_immediate_presentation=False)
    else:
        sys.stdout.write(NO_WORDS_MESSAGE)

def api_select_top(words, selection, unstressed, exclude_real, ignore_syllables):
    output = []
    i = 0
    no_words_returned = True

    while len(output) < selection:
        if i == len(words):
            output.append(TOO_FEW_MESSAGE)
            break
        else:
            word, score = words[i]
            result = select_for_web(word, score, unstressed, exclude_real, ignore_syllables)

            i += 1

            if result:
                no_words_returned = False
                output.append(result)

    if no_words_returned:
        output = [NO_WORDS_MESSAGE]

    return output

def api_select_random(words, selection, unstressed, exclude_real, ignore_syllables):
    output = []

    while len(output) < selection:
        i = int(random.random() * len(words))

        word, score = words[i]
        result = select_for_web(word, score, unstressed, exclude_real, ignore_syllables)

        if result:
            output.append(result)

    if len(output) == 0:
        output = [NO_WORDS_MESSAGE]

    return output
