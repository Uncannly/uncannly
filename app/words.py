import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.present import Present
from lib.secondary_data_io import load
from lib.type_conversion import string_to_array, kebab_to_snake

def get(return_count,	averaging, random_selection, unweighted, exclude_real):

	return_count = int(return_count) if return_count else 45
	filtering = 'averaging' if averaging != None else 'continued_product'
	random_selection = random_selection != None
	weighting = 'unweighted' if unweighted != None else 'weighted'
	exclude_real = exclude_real != None

	most_probable_words = load(
		'most_probable_words_by_{}_{}'.format(filtering, weighting)
	)
	
	if random_selection:
		output = []
		words = most_probable_words.keys()
		while len(output) < return_count:
			random_word = random.choice(words)
			arrayified_word = string_to_array(random_word)
			result = Present.for_web(arrayified_word, exclude_real)
			if result:
				output.append(result) 
		return output
	else:
		top_words = sorted(
			most_probable_words,
			key = most_probable_words.get,
			reverse = True
		)
		output = []
		i = 0
		while len(output) < return_count:
			arrayified_word = string_to_array(top_words[i])
			i += 1
			result = Present.for_web(arrayified_word, exclude_real)
			if result:
				output.append(result) 	
		return output