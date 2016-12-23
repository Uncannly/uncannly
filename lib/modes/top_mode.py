import random
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.present import Present
from lib.type_conversion import string_to_array
from data.load_data import load_scores

TOO_FEW_MESSAGE = 'Fewer words met criteria than the specified return count.\n'
NO_WORDS_MESSAGE = 'No words met criteria.\n'

class TopMode(object):
  @staticmethod
  def get(interface,
          pool,
          selection,
          scoring_method,
          score_threshold,
          unweighted,
          unstressed,
          exclude_real):

    most_probable_words = load_scores(scoring_method, unweighted, unstressed)
    most_probable_words.sort(key=lambda x: -x[1])
    most_probable_words = most_probable_words[0:int(pool)]

    if selection:
      selector = api_select_random if interface == 'api' else cli_select_random
    else:
      selection = pool
      selector = api_select_top if interface == 'api' else cli_select_top

    words = []
    for word, score in most_probable_words:
      if score < score_threshold:
        break
      else:
        words.append(word)

    return selector(words, selection, unstressed, exclude_real)

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
    arrayified_word = string_to_array(words[i])
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
    arrayified_word = string_to_array(random.choice(words))
    result = Present.for_web(arrayified_word, unstressed, exclude_real)
    if result:
      output.append(result)

  if len(output) == 0:
    output = [NO_WORDS_MESSAGE]

  return output
