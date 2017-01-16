import sys
import random
import ast

from lib.present import for_web, for_terminal, for_web_syllables, for_terminal_syllables
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
    resulter = for_terminal if ignore_syllables else for_terminal_syllables

    if len(words) > 0:
        i = 0
        for _ in xrange(selection):
            presented = False
            while not presented:
                if i == len(words):
                    return sys.stdout.write(TOO_FEW_MESSAGE)

                if not ignore_syllables:
                    words[i] = (ast.literal_eval(words[i][0]), words[i][1])

                presented = resulter(words[i], unstressed, exclude_real, False)

                i += 1
    else:
        sys.stdout.write(NO_WORDS_MESSAGE)

def cli_select_random(words, selection, unstressed, exclude_real, ignore_syllables):
    resulter = for_terminal if ignore_syllables else for_terminal_syllables

    if len(words) > 0:
        for _ in xrange(selection):
            presented = False
            while not presented:
                word = random.choice(words)
                if not ignore_syllables:
                    word = (ast.literal_eval(word[0]), word[1])

                presented = resulter(word, unstressed, exclude_real, False)
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
            if ignore_syllables:
                arrayified_word = (string_to_array(words[i][0]), words[i][1])
                result = for_web(arrayified_word, unstressed, exclude_real)
            else:
                care_about = (ast.literal_eval(words[i][0]), words[i][1])
                result = for_web_syllables(care_about, unstressed, exclude_real)

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
        if ignore_syllables:
            arrayified_word = (string_to_array(words[i][0]), words[i][1])
            result = for_web(arrayified_word, unstressed, exclude_real)
        else:
            care_about = (ast.literal_eval(words[i][0]), words[i][1])
            result = for_web_syllables(care_about, unstressed, exclude_real)
        if result:
            output.append(result)

    if len(output) == 0:
        output = [NO_WORDS_MESSAGE]

    return output
