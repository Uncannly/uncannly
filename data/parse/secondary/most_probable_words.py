import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from lib.type_conversion import array_to_string
from lib.score import get_score

default_limit_for_scoring_method = {
	'with_stress': {
		'weighted': {
			'integral_product': 8.1   * 10**-16, # 10079 
			'integral_sum':     6.35  * 10**-2,  # 10831 
			'mean_geometric':   3.1   * 10**-4,  # 10173 
			'mean_arithmetic':  2.69  * 10**-1   # 11105 
		},
		'unweighted': {
			'integral_product': 1.3   * 10**-17, # 10039
			'integral_sum':     5.85  * 10**-2,  # 10208
			'mean_geometric':   3.0   * 10**-5,  # 10504
			'mean_arithmetic':  1.99  * 10**-1   # 12442
		}
	},
	'stressless': {
		'weighted': {
			'integral_product': 9.97  * 10**-16, # 11339
			'integral_sum':     6.4   * 10**-2,  # 10809
			'mean_geometric':   3.1   * 10**-4,  # 10773
			'mean_arithmetic':  2.69  * 10**-1   # 10506
		},
		'unweighted': {
			'integral_product': 3.5   * 10**-17, # 10264
			'integral_sum':     5.9   * 10**-2,  # 10284
			'mean_geometric':   9.0   * 10**-5,  # 10849
			'mean_arithmetic':  1.98  * 10**-1   # 12120
		}
	}
}

class MostProbableWords:

	@staticmethod
	def get(most_probable_next_phonemes, stressless, unweighted, method_mean, method_addition):

		stress_consideration = 'stressless' if stressless else 'with_stress'
		frequency_weighting = 'unweighted' if unweighted else 'weighted'
		if method_mean:
			scoring_method = 'mean_arithmetic' if method_addition else 'mean_geometric'
		else:
			scoring_method = 'integral_sum' if method_addition else 'integral_product'
		limit = default_limit_for_scoring_method[stress_consideration][frequency_weighting][scoring_method]

		most_probable_words = []

		def next_phoneme(word, score):
			word_length = len(word)
			current_phoneme = word[word_length - 1]

			if word_length > 20:
				pass
			else:
				for (phoneme, probability) in most_probable_next_phonemes[current_phoneme]:
					score = get_score(score, scoring_method, probability, word_length)		
					if score < limit:
						pass
					elif phoneme == 'END_WORD':
						stringified_word = array_to_string(word[1:len(word)])
						most_probable_words.append((stringified_word, score))
					else:	
						grown_word = word[:]
						grown_word.append(phoneme)
						next_phoneme(grown_word, score)

		next_phoneme(['START_WORD'], 1.0)

		most_probable_words.sort(key=lambda x: -x[1])

		return most_probable_words[:1000]