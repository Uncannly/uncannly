import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from lib import format

def parse(most_probable_next_phonemes, filter):
	most_probable_words = {}

	if (filter == 'continued_product'):
		limit = 0.0000000000000000000001
	elif (filter == 'averaging'):
		limit = 0.2415

	def next_phoneme(word, word_probability):
		word_length = len(word)
		current_phoneme = word[word_length - 1]

		if word_length > 20:
			pass
		else:
			for pp_tuple in most_probable_next_phonemes[current_phoneme]:
				phoneme = pp_tuple[0]
				probability = pp_tuple[1]

				if (filter == 'continued_product'):
					word_probability *= probability
				elif (filter == 'averaging'):
					word_probability = (word_length * word_probability + probability) \
						/ (word_length + 1)

				if word_probability < limit:
					pass
				elif phoneme == 'END_WORD':
					formatted_word = format.format(word)
					most_probable_words[formatted_word] = word_probability
				else:	
					grown_word = word[:]
					grown_word.append(phoneme)
					next_phoneme(grown_word, word_probability)

	next_phoneme(['START_WORD'], 1.0)

	return most_probable_words