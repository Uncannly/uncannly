import random

import file, format, present

def share(filter, frequency_weighting):
	most_probable_words = file.load('most_probable_words_by_{}_{}'.format(filter, frequency_weighting))

	words = most_probable_words.keys()

	print 'total generated most probable words:', len(words)

	while True:
		word = random.choice(words)
		present.present(word)