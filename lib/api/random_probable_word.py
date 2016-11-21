import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import random_probable_word

def get():
	return random_probable_word.get()