import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import random_probable_word

def get(include_real_words):
	print include_real_words
	return random_probable_word.get(include_real_words, multiple=False)