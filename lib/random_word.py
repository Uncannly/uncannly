import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from present import Present
from type_conversion import array_to_string
from next_phoneme import next_phoneme

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
					word = [phoneme]
			elif interface == "api":
				word_to_present = Present.for_web(word, exclude_real)
				if word_to_present != None:
					return word_to_present
				else:
					phoneme = 'START_WORD'
					word = [phoneme]
		else:
			word.append(phoneme)