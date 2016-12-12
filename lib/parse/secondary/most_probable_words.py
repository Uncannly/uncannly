import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from lib.type_conversion import array_to_string

class MostProbableWords:
	@staticmethod
	def by_mean_arithmetic(most_probable_next_phonemes):
		return parse(most_probable_next_phonemes, 'mean_arithmetic')

	@staticmethod
	def by_integral_product(most_probable_next_phonemes):
		return parse(most_probable_next_phonemes, 'integral_product')

def parse(most_probable_next_phonemes, scoring_method):
	most_probable_words = {}

	if (scoring_method == 'integral_product'):
		limit = 0.0000000000000000000001
	elif (scoring_method == 'mean_arithmetic'):
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

				if (scoring_method == 'integral_product'):
					word_probability *= probability
				elif (scoring_method == 'mean_arithmetic'):
					word_probability = (word_length * word_probability + probability) \
						/ (word_length + 1)

				if word_probability < limit:
					pass
				elif phoneme == 'END_WORD':
					stringified_word = array_to_string(word[1:len(word)])
					most_probable_words[stringified_word] = word_probability
				else:	
					grown_word = word[:]
					grown_word.append(phoneme)
					next_phoneme(grown_word, word_probability)

	next_phoneme(['START_WORD'], 1.0)

	return most_probable_words