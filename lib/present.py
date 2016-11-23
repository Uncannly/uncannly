import time

from ipa import ipa
from type_conversion import array_to_string
from secondary_data_io import load

words = load('words')
word_pronunciations = load('word_pronunciations')

class Present:
	@staticmethod
	def for_web(word, include_real_words):
		ipa_word = ipa(word[1:])
		
		stringified_word = array_to_string(word)
		existing_word = already_in_dictionary(stringified_word)
		
		return present_word(ipa_word, existing_word, include_real_words)

	@staticmethod
	def for_terminal(word, include_real_words):
		existing_word = already_in_dictionary(word)
		print present_word(word, existing_word, include_real_words)
		time.sleep(0.2)

def present_word(word, existing_word=True, include_real_words=True):
	if existing_word:
		if include_real_words == True:
			return '{} (word exists already: {})'.format(word, existing_word)
		else:
			return None
	else:
		return word

def already_in_dictionary(word):
	if word in word_pronunciations:
		index = word_pronunciations.index(word)
		return words[index]