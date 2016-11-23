import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.present import Present
from next_phoneme import next_phoneme

def get(multiple=False):
	phoneme = 'START_WORD'
	word = [phoneme]
	while True:
		phoneme = next_phoneme(phoneme, random.random())
		if phoneme == 'END_WORD':
			if multiple:
				Present.for_terminal(word)
				phoneme = 'START_WORD'
				word = [phoneme]
			else:
				return Present.for_web(word, True)
		else:
			word.append(phoneme)