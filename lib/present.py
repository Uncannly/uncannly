import time

import file, ipa, format

words = file.load('words')
word_pronunciations = file.load('word_pronunciations')

def already_in_dictionary(word):
	if word in word_pronunciations:
		index = word_pronunciations.index(word)
		return words[index]

def present(word):
	formatted_word = format.format(word)
	existing_word = already_in_dictionary(formatted_word)
	ipa_word = ipa.ipa(word[1:])
	if existing_word:
		print '{} (word exists already: {})'.format(ipa_word, existing_word)
	else:
		print ipa_word
	time.sleep(0.2)

def present_for_web(word):
	formatted_word = format.format(word)
	existing_word = already_in_dictionary(formatted_word)
	ipa_word = ipa.ipa(word[1:])
	if existing_word:
		return '{} (word exists already: {})'.format(ipa_word, existing_word)
	else:
		return ipa_word