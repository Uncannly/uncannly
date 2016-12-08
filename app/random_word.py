import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import random_word

def get(unweighted, exclude_real):

	unweighted = unweighted != None
	exclude_real = exclude_real != None

	return random_word.get("api", unweighted, exclude_real)