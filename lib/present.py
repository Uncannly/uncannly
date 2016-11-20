import time

import file

words = file.load('words')
word_pronunciations = file.load('word_pronunciations')

def already_in_dictionary(word):
	if word in word_pronunciations:
		index = word_pronunciations.index(word)
		return words[index]

def present(word):
	existing_word = already_in_dictionary(word)
	if existing_word:
		print '{} (word exists already: {})'.format(word, existing_word)
	else:
		print word
	time.sleep(0.2)