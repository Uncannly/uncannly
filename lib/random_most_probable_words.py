import random

import file, format, present

def share(filter):
	most_probable_words = file.load('most_probable_words_by_{}'.format(filter))

	words = most_probable_words.keys()

	print 'total generated most probable words:', len(words)

	while True:
		present.present(random.choice(words))