import random, time, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import random_probable_word

def get():
	random_probable_word.get(multiple=True)