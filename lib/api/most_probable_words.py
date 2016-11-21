import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import file, present

def get(style, filter, weighted_by_frequency, include_real_words, return_count):
	frequency_weighting = 'weighted' if weighted_by_frequency else 'unweighted'
	most_probable_words = file.load(
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
			result = present.present_for_web(
				sorted_words[i].split(' '), 
				include_real_words
			)
			if result:
				output.append(result) 	
		return output
	else:
		output = []
		words = most_probable_words.keys()
		while len(output) < int(return_count):
			random_word = random.choice(words)
			result = present.present_for_web(
				random_word.split(' '), 
				include_real_words
			)
			if result:
				output.append(result) 
		return output