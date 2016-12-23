import sys

from lib.ipa import ipa
from lib.type_conversion import array_to_string
from data.load_data import load_words

words = load_words()

class Present:
  @staticmethod
  def for_web(word, unstressed, exclude_real):
    ipa_word = ipa(word)

    stringified_word = array_to_string(word)
    existing_word = already_in_dictionary(stringified_word, unstressed)

    return present_word(ipa_word, exclude_real, existing_word)

  @staticmethod
  def for_terminal(word, unstressed, exclude_real, suppress_immediate):
    existing_word = already_in_dictionary(word, unstressed)
    word = present_word(word, exclude_real, existing_word)
    if word == False:
      return False
    else:
      if not suppress_immediate:
        sys.stdout.write(word + '\n')
      return word

def present_word(word, exclude_real, existing_word):
  if existing_word:
    return False if exclude_real else '{} ({})'.format(word, existing_word)
  else:
    return word

def already_in_dictionary(word, unstressed):
  for (spelling, pronunciation) in words:
    if unstressed:
      pronunciation = replace_multiple(pronunciation, '012')
    if word == pronunciation:
      return spelling

def replace_multiple(string, characters):
  characters = "012"
  for character in characters:
    if character in string:
      string = string.replace(character, "\\" + character)
