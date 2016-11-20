import file

phonetic_words = file.load('phonetic_words')
words = file.load('words')

def already_in_dictionary(word):
	if word in phonetic_words:
		index = phonetic_words.index(word)
		return words[index]