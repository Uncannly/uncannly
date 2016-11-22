import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.present import present, present_for_web
from next_phoneme import next_phoneme

def get(multiple=False):
	phoneme = 'START_WORD'
	word = [phoneme]
	while True:
		phoneme = next_phoneme(phoneme, random.random())
		if phoneme == 'END_WORD':
			if multiple:
				present(word)
				phoneme = 'START_WORD'
				word = [phoneme]
			else:
				return present_for_web(word, True)
		else:
			word.append(phoneme)