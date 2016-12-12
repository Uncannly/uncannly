import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from lib.type_conversion import array_to_string

default_limit_for_scoring_method = {
	'weighted': {
		'integral_product': 1     * 10**-22, # 1056044 total returned
		'integral_sum':     4.44  * 10**-2,  # 1167773 total returned
		'mean_geometric':   1     * 10**-4,  # 1024405 total returned
		'mean_arithmetic':  2.415 * 10**-1   # 1034046 total returned
	},
	'unweighted': {
		'integral_product': 8     * 10**-25, # 1016069 total returned
		'integral_sum':     4.1   * 10**-2,  # 1105730 total returned
		'mean_geometric':   2.75  * 10**-5,  # 1016940 total returned
		'mean_arithmetic':  1.845 * 10**-1   # 1031604 total returned
	}
}

class MostProbableWords:
	@staticmethod
	def by_integral_product(most_probable_next_phonemes, frequency_weighting):
		return parse(most_probable_next_phonemes, frequency_weighting, 'integral_product')

	@staticmethod
	def by_integral_sum(most_probable_next_phonemes, frequency_weighting):
		return parse(most_probable_next_phonemes, frequency_weighting, 'integral_sum')

	@staticmethod
	def by_mean_geometric(most_probable_next_phonemes, frequency_weighting):
		return parse(most_probable_next_phonemes, frequency_weighting, 'mean_geometric')

	@staticmethod
	def by_mean_arithmetic(most_probable_next_phonemes, frequency_weighting):
		return parse(most_probable_next_phonemes, frequency_weighting, 'mean_arithmetic')

def parse(most_probable_next_phonemes, frequency_weighting, scoring_method):
	most_probable_words = {}

	limit = default_limit_for_scoring_method[frequency_weighting][scoring_method]

	def next_phoneme(word, score):
		word_length = len(word)
		current_phoneme = word[word_length - 1]

		if word_length > 20:
			pass
		else:
			for (phoneme, probability) in most_probable_next_phonemes[current_phoneme]:
				if (scoring_method == 'integral_product'):
					score = score * probability
				elif (scoring_method == 'integral_sum'):
					score = 1 / ((1 / score) + (1 - probability))
				elif (scoring_method == 'mean_geometric'):
					previous_weighted_probability = score ** word_length
					multiply_in_new_probability = previous_weighted_probability * probability
					root = 1.0 / float(word_length)
					score = multiply_in_new_probability ** root
				elif (scoring_method == 'mean_arithmetic'):
					score = ((score * (word_length)) + probability) / (word_length + 1)
			
				if score < limit:
					pass
				elif phoneme == 'END_WORD':
					stringified_word = array_to_string(word[1:len(word)])
					most_probable_words[stringified_word] = score
				else:	
					grown_word = word[:]
					grown_word.append(phoneme)
					next_phoneme(grown_word, score)

	next_phoneme(['START_WORD'], 1.0)

	sorted_most_probable_words = sorted(
		most_probable_words,
		key=most_probable_words.get,
		reverse=True
	)

	sorted_most_probable_words_with_score = []
	for word in sorted_most_probable_words:
		sorted_most_probable_words_with_score.append(
			(word, most_probable_words[word])
		)

	return sorted_most_probable_words_with_score
