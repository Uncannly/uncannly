import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.present import Present
from lib.secondary_data_io import load

def share(filter, frequency_weighting, include_real_words):
	most_probable_words = load(
		'most_probable_words_by_{}_{}'.format(filter, frequency_weighting)
	)

	print 'total generated most probable words:', len(most_probable_words)

	sorted_most_probable_words = sorted(
		most_probable_words,
		key = most_probable_words.get,
		reverse = True
	)

	for word in sorted_most_probable_words:
		Present.for_terminal(word, include_real_words)