import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import file

def get(style, filter, weighted_by_frequency, return_count):
	frequency_weighting = 'weighted' if weighted_by_frequency else 'unweighted'
	most_probable_words = file.load(
		'most_probable_words_by_{}_{}'.format(filter, frequency_weighting)
	)
	if style == 'sorted':
		return sorted(
			most_probable_words,
			key = most_probable_words.get,
			reverse = True
		)[0:int(return_count)]
	else:
		output = []
		words = most_probable_words.keys()
		for i in range(0, int(return_count)):
			output.append(random.choice(words))
		return output