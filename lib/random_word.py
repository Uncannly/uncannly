import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from present import Present
from secondary_data_io import load
from type_conversion import array_to_string

next_phonemes_weighted = load('most_probable_next_phonemes')
next_phonemes_unweighted = load('most_probable_next_phonemes_unweighted')

class RandomWord:
	@staticmethod
	def get(interface, unweighted, exclude_real):
		phoneme = 'START_WORD'
		word = []
		while True:
			phoneme = next_phoneme(phoneme, random.random(), unweighted)
			if phoneme == 'END_WORD':
				if interface == "bin":
					stringified_word = array_to_string(word)
					word_was_presented = Present.for_terminal(stringified_word, exclude_real)
					if word_was_presented == True:
						return
					else:
						phoneme = 'START_WORD'
						word = []
				elif interface == "api":
					word_to_present = Present.for_web(word, exclude_real)
					if word_to_present != None:
						return word_to_present
					else:
						phoneme = 'START_WORD'
						word = []
			else:
				word.append(phoneme)

def next_phoneme(phoneme, random_number, unweighted):
	next_phonemes = next_phonemes_unweighted if unweighted else next_phonemes_weighted

	accumulated_probability = 0
	for (phoneme, probability) in next_phonemes[phoneme]:
	  accumulated_probability += probability
	  if accumulated_probability >= random_number:
	  	return phoneme