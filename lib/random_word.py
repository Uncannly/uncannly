import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from present import Present
from type_conversion import array_to_string
from next_phoneme import next_phoneme

def get(interface, weighted_by_frequency, include_real_words):
	phoneme = 'START_WORD'
	word = [phoneme]
	while True:
		phoneme = next_phoneme(phoneme, random.random(), weighted_by_frequency)
		if phoneme == 'END_WORD':
			if interface == "bin":
				stringified_word = array_to_string(word)
				Present.for_terminal(stringified_word, include_real_words)
				return
				# phoneme = 'START_WORD'
				# word = [phoneme]
			elif interface == "api":
				word_to_present = Present.for_web(word, include_real_words)
				if word_to_present != None:
					return word_to_present
				else:
					phoneme = 'START_WORD'
					word = [phoneme]
		else:
			word.append(phoneme)