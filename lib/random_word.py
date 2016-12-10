import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from present import Present
from secondary_data_io import load
from type_conversion import array_to_string

weighted_distributions = load('cumulative_distributions')
unweighted_distributions = load('cumulative_distributions_unweighted')

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
	distributions = unweighted_distributions if unweighted else weighted_distributions
	
	return next(step['next_phoneme']
		for step in distributions[phoneme]
		if step['accumulated_probability'] >= random_number
	)