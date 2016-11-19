import random, time, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import file

phoneme_chain_prob = file.load('phoneme_probabilities')
phonetic_words = file.load('phonetic_words')
words = file.load('words')

def get_next_phoneme(phoneme, random_number):
	current_next_phoneme_chance = 2.0
	current_next_phoneme = ''
	for transition_phoneme, chance in phoneme_chain_prob[phoneme].iteritems():
		if chance >= random_number and chance < current_next_phoneme_chance:
			current_next_phoneme_chance = chance
			current_next_phoneme = transition_phoneme
	return current_next_phoneme

def present(word_arr):
	word = ' '.join(word_arr[1:(len(word_arr))])
	if word in phonetic_words:
		index = phonetic_words.index(word)
		print '{} (word exists already: {})'.format(word, words[index])
	else:
		print word

word = ['START_WORD']
while True:
	next_phoneme = get_next_phoneme(word[len(word)-1], random.random())
	if next_phoneme == 'END_WORD':
		present(word)
		word = ['START_WORD']
		time.sleep(.5)
	else:
		word.append(next_phoneme)
		phoneme = next_phoneme