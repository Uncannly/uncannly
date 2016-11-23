import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.present import Present
from lib.secondary_data_io import load
from lib.type_conversion import string_to_array

def get(style, filter, weighted_by_frequency, include_real_words, return_count):
	frequency_weighting = 'weighted' if weighted_by_frequency else 'unweighted'
	most_probable_words = load(
		'most_probable_words_by_{}_{}'.format(filter, frequency_weighting)
	)
	if style == 'sorted':
		sorted_words = sorted(
			most_probable_words,
			key = most_probable_words.get,
			reverse = True
		)
		output = []
		i = 0
		while len(output) < int(return_count):
			i += 1
			arrayified_word = string_to_array(sorted_words[i])
			result = Present.for_web(arrayified_word, include_real_words)
			if result:
				output.append(result) 	
		return output
	else:
		output = []
		words = most_probable_words.keys()
		while len(output) < int(return_count):
			random_word = random.choice(words)
			arrayified_word = string_to_array(random_word)
			result = Present.for_web(arrayified_word, include_real_words)
			if result:
				output.append(result) 
		return output