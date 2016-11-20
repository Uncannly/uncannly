import random

import file, format, present

def share(style):
	most_probable_words = file.load('most_probable_words_by_{}'.format(style))

	words = most_probable_words.keys()

	print 'total generated most probable words:', len(words)

	while True:
		present.present(random.choice(words))