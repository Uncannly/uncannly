import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from lib.type_conversion import array_to_string
from lib.score import get_score
from lib.options import booleans_to_strings, scoring_methods, default_limits, pool_max

class MostProbableWords:

	@staticmethod
	def get(next_phonemes, options):
		unstressed, unweighted, method_mean, method_addition = options
		
		stressing, weighting = booleans_to_strings(unstressed, unweighted)

		scoring_method = scoring_methods.keys()[
			scoring_methods.values().index((method_mean, method_addition))
		]

		limit = default_limits[stressing][weighting][scoring_method]

		most_probable_words = []

		def next_phoneme(word, score):
			word_length = len(word)
			current_phoneme = word[word_length - 1]

			if word_length > 20:
				pass
			else:
				for (phoneme, probability) in next_phonemes[current_phoneme]:
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

		return most_probable_words[:pool_max]