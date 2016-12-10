import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.random_word import RandomWord

def get(unweighted, exclude_real):

	unweighted = unweighted != None
	exclude_real = exclude_real != None

	return RandomWord.get("api", unweighted, exclude_real)