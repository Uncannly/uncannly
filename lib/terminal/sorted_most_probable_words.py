import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import file, format, present

def share(filter, frequency_weighting):
	most_probable_words = file.load('most_probable_words_by_{}_{}'.format(filter, frequency_weighting))

	print 'total generated most probable words:', len(most_probable_words)

	sorted_most_probable_words = sorted(
		most_probable_words,
		key = most_probable_words.get,
		reverse = True
	)

	for word in sorted_most_probable_words:
		present.present(word)