import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.present import Present
from lib.secondary_data_io import load

def share(filter, frequency_weighting):
	most_probable_words = load('most_probable_words_by_{}_{}'.format(filter, frequency_weighting))

	words = most_probable_words.keys()

	print 'total generated most probable words:', len(words)

	while True:
		word = random.choice(words)
		Present.for_terminal(word, include_real_words=True)