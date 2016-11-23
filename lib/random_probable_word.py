import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.present import Present
from next_phoneme import next_phoneme

def get(include_real_words, multiple=False):
	phoneme = 'START_WORD'
	word = [phoneme]
	while True:
		phoneme = next_phoneme(phoneme, random.random())
		if phoneme == 'END_WORD':
			if multiple == True:
				Present.for_terminal(word, include_real_words)
				phoneme = 'START_WORD'
				word = [phoneme]
			else:
				word_to_present = Present.for_web(word, include_real_words)
				if word_to_present != None:
					return word_to_present
				else:
					phoneme = 'START_WORD'
					word = [phoneme]
		else:
			word.append(phoneme)