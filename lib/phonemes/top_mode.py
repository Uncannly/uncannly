import sys
import random

from lib.present import for_web, for_terminal
from lib.conversion import string_to_array
from lib.options import TOO_FEW_MESSAGE, NO_WORDS_MESSAGE, POOL_DEFAULT
from data.load_data import load_scores

# pylint: disable=too-many-instance-attributes,too-few-public-methods
class TopModePhonemes(object):
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
            length = len(string_to_array(word))
            if score < self.score_threshold:
                break
            elif self.min_length is not None and length < self.min_length:
                pass
            elif self.max_length is not None and length > self.max_length:
                pass
            elif word in words:
                pass
            else:
                words.append((word, score))

        return selector(words, self.selection, self.unstressed, self.exclude_real)
# pylint: enable=too-many-instance-attributes,too-few-public-methods

def cli_select_top(words, selection, unstressed, exclude_real):
    if len(words) > 0:
        i = 0
        for _ in xrange(selection):
            presented = False
            while not presented:
                if i == len(words):
                    return sys.stdout.write(TOO_FEW_MESSAGE)
                presented = for_terminal(words[i],
                                         unstressed,
                                         exclude_real,
                                         False)

                i += 1
    else:
        sys.stdout.write(NO_WORDS_MESSAGE)

def cli_select_random(words, selection, unstressed, exclude_real):
    if len(words) > 0:
        for _ in xrange(selection):
            while not for_terminal(random.choice(words),
                                   unstressed,
                                   exclude_real,
                                   False):
                pass
    else:
        sys.stdout.write(NO_WORDS_MESSAGE)

def api_select_top(words, selection, unstressed, exclude_real):
    output = []
    i = 0
    no_words_returned = True

    # attempts = 0
    while len(output) < selection:

        # this whole section was not necessary before syllables. why does this happen?
        # attempts += 1
        # if attempts > 100000:
        #     break

        if i == len(words):
            output.append(TOO_FEW_MESSAGE)
            break

        # # this is also a syllables-related siutation
        # # print words[i][0]
        # if len(words[i][0]) == 0:
        #     print 'it happened....'

        else:
            # print words[i][1]
            arrayified_word = (string_to_array(words[i][0]), words[i][1])
            # print arrayified_word
            i += 1
            result = for_web(arrayified_word, unstressed, exclude_real)
            if result:
                no_words_returned = False
                output.append(result)

    if no_words_returned:
        output = [NO_WORDS_MESSAGE]

    return output

def api_select_random(words, selection, unstressed, exclude_real):
    output = []
    while len(output) < selection:
        i = int(random.random() * len(words))
        arrayified_word = (string_to_array(words[i][0]), words[i][1])
        result = for_web(arrayified_word, unstressed, exclude_real)
        if result:
            output.append(result)

    if len(output) == 0:
        output = [NO_WORDS_MESSAGE]

    return output
