import file

words = file.load('words')
word_pronunciations = file.load('word_pronunciations')

def already_in_dictionary(word):
	if word in word_pronunciations:
		index = word_pronunciations.index(word)
		return words[index]