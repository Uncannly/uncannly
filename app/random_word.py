import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import random_word

def get(weighted_by_frequency, include_real_words):
	return random_word.get("api", weighted_by_frequency, include_real_words)