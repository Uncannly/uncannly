import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import file, present

cumulative_distributions = file.load('cumulative_distributions')

def next_phoneme(phoneme, random_number):
	return next(step['next_phoneme']
		for step in cumulative_distributions[phoneme]
		if step['accumulated_probability'] >= random_number
	)

def get():
	phoneme = 'START_WORD'
	word = [phoneme]
	while True:
		phoneme = next_phoneme(phoneme, random.random())
		if phoneme == 'END_WORD':
			return present.present_for_web(word)
		else:
			word.append(phoneme)