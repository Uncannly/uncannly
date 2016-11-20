import random, time, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import file, format, exists

cumulative_distributions = file.load('cumulative_distributions')

def next_phoneme(phoneme, random_number):
	return next(step['next_phoneme']
		for step in cumulative_distributions[phoneme]
		if step['accumulated_probability'] >= random_number
	)

def present(word):
	word = format.format(word)
	existing_word = exists.already_in_dictionary(word)
	if existing_word:
		print '{} (word exists already: {})'.format(word, existing_word)
	else:
		print word

phoneme = 'START_WORD'
word = [phoneme]
while True:
	phoneme = next_phoneme(phoneme, random.random())
	if phoneme == 'END_WORD':
		present(word)
		phoneme = 'START_WORD'
		word = [phoneme]
		time.sleep(0.2)
	else:
		word.append(phoneme)