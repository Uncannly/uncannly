import time, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import file, format

most_probable_next_phonemes = file.load('most_probable_next_phonemes')

def next_phoneme(word):
	current_phoneme = word[len(word) - 1]

	if (current_phoneme == 'END_WORD' or len(word) > 20):
		print format.format(word)
	else:
		for phoneme in most_probable_next_phonemes[current_phoneme]:
			grown_word = word[:]
			grown_word.append(phoneme)
			next_phoneme(grown_word)

next_phoneme(['START_WORD'])