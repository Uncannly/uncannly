import sys

from ipa import ipa
from type_conversion import array_to_string
from secondary_data_io import load

words = load('words')
word_pronunciations = load('word_pronunciations')
word_pronunciations_stressless = load('word_pronunciations_stressless')

class Present:
	@staticmethod
	def for_web(word, ignore_stress, exclude_real):
		ipa_word = ipa(word)
		
		stringified_word = array_to_string(word)
		existing_word = already_in_dictionary(stringified_word, ignore_stress)
		
		return present_word(ipa_word, exclude_real, existing_word)

	@staticmethod
	def for_terminal(word, ignore_stress, exclude_real):
		existing_word = already_in_dictionary(word, ignore_stress)
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

def already_in_dictionary(word, ignore_stress):
	pronunciations = word_pronunciations_stressless if ignore_stress else word_pronunciations
	if word in pronunciations:
		index = pronunciations.index(word)
		return words[index]