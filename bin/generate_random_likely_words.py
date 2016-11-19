import random, time, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import file, format

phoneme_probabilities = file.load('phoneme_probabilities')
phonetic_words = file.load('phonetic_words')
words = file.load('words')

# THIS VERSION ONLY WORKS IF THE PROBABILITIES ARE ORDERED, 
# WHICH THEY MOSTLY ARE BUT NOT PERFECTLY...
# def next_phoneme(current_phoneme, random_number):
# 	return next(phoneme
# 		for phoneme, probability 
# 		in phoneme_probabilities[current_phoneme].iteritems() 
# 		if probability >= random_number
# 	)

def next_phoneme(phoneme, random_number):
	current_next_phoneme_chance = 2.0
	current_next_phoneme = ''
	for transition_phoneme, chance in phoneme_probabilities[phoneme].iteritems():
		if chance >= random_number and chance < current_next_phoneme_chance:
			current_next_phoneme_chance = chance
			current_next_phoneme = transition_phoneme
	return current_next_phoneme

def test_for_orderedness(phoneme):
	previous_phoneme = ''
	previous_chance = 0
	for next_phoneme, next_chance in phoneme_probabilities[phoneme].iteritems():
		print next_phoneme, next_chance
		if next_chance < previous_chance:
			print 'what'
		previous_phoneme = next_phoneme
		previous_chance = next_chance

def present(word):
	word = format.format(word)
	if word in phonetic_words:
		index = phonetic_words.index(word)
		print '{} (word exists already: {})'.format(word, words[index])
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

test_for_orderedness('IY')