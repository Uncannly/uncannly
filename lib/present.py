import sys

from ipa import ipa
from type_conversion import array_to_string
from secondary_data_io import load

words = load('words')
word_pronunciations = load('word_pronunciations')

class Present:
	@staticmethod
	def for_web(word, exclude_real):
		ipa_word = ipa(word)
		
		stringified_word = array_to_string(word)
		existing_word = already_in_dictionary(stringified_word)
		
		return present_word(ipa_word, exclude_real, existing_word)

	@staticmethod
	def for_terminal(word, exclude_real):
		existing_word = already_in_dictionary(word)
		word = present_word(word, exclude_real, existing_word)
		if word != None:
			sys.stdout.write(word + '\n')
			return True
		else:
			return False

def present_word(word, exclude_real, existing_word):
	if existing_word:
		return None if exclude_real else '{} ({})'.format(word, existing_word)
	else:
		return word

def already_in_dictionary(word):
	if word in word_pronunciations:
		index = word_pronunciations.index(word)
		return words[index]