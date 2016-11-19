import time, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import file

phoneme_chain_prob = file.load('ranked_most_likely_next_phonemes_per_phoneme')

def present(word):
	return ' '.join(word[1:(len(word)-1)])

def next_phoneme(current_word, level):
	current_phoneme = current_word[len(current_word) - 1]

	if (current_phoneme == 'END_WORD' or len(current_word) > 20):
		print present(current_word)
	else:
		for phoneme in phoneme_chain_prob[current_phoneme]:
			grown_word = current_word[:]
			grown_word.append(phoneme)
			next_phoneme(grown_word, level + 1)

next_phoneme(['START_WORD'], 1)