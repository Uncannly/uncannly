import time, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import file

ranked_most_likely_next_phonemes_per_phoneme = file.load('ranked_most_likely_next_phonemes_per_phoneme')

def present(word):
	return ' '.join(word[1:(len(word)-1)])

def next_phoneme(word):
	current_phoneme = word[len(word) - 1]

	if (current_phoneme == 'END_WORD' or len(word) > 20):
		print present(word)
	else:
		for phoneme in ranked_most_likely_next_phonemes_per_phoneme[current_phoneme]:
			grown_word = word[:]
			grown_word.append(phoneme)
			next_phoneme(grown_word)

next_phoneme(['START_WORD'])