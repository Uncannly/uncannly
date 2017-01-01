import random
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.present import Present
from lib.type_conversion import string_to_array
from lib.options import TOO_FEW_MESSAGE, NO_WORDS_MESSAGE
from data.load_data import load_scores

# pylint: disable=too-many-instance-attributes,too-few-public-methods
class TopMode(object):
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

    def get(self):

        most_probable_words = load_scores(self.scoring_method,
                                          self.ignore_length,
                                          self.ignore_position,
                                          self.unstressed,
                                          self.unweighted)
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
                presented = Present.for_terminal(word=words[i],
                                                 unstressed=unstressed,
                                                 exclude_real=exclude_real,
                                                 suppress_immediate=False)

                i += 1
    else:
        sys.stdout.write(NO_WORDS_MESSAGE)

def cli_select_random(words, selection, unstressed, exclude_real):
    if len(words) > 0:
        for _ in xrange(selection):
            while not Present.for_terminal(word=random.choice(words),
                                           unstressed=unstressed,
                                           exclude_real=exclude_real,
                                           suppress_immediate=False):
                pass
    else:
        sys.stdout.write(NO_WORDS_MESSAGE)

def api_select_top(words, selection, unstressed, exclude_real):
    output = []
    i = 0
    no_words_returned = True
    while len(output) < selection:
        if i == len(words):
            output.append(TOO_FEW_MESSAGE)
            break
        arrayified_word = (string_to_array(words[i][0]), words[i][1])
        i += 1
        result = Present.for_web(arrayified_word, unstressed, exclude_real)
        if result:
            no_words_returned = False
            output.append(result)

    if no_words_returned:
        output = [NO_WORDS_MESSAGE]

    return output

def api_select_random(words, selection, unstressed, exclude_real):
    output = []
    while len(output) < selection:
        i = int(random.random * len(words))
        arrayified_word = (string_to_array(words[i][0]), words[i][1])
        result = Present.for_web(arrayified_word, unstressed, exclude_real)
        if result:
            output.append(result)

    if len(output) == 0:
        output = [NO_WORDS_MESSAGE]

    return output
