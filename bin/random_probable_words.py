import random, time, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import random_probable_word

random_probable_word.get(
	weighted_by_frequency=True,
	include_real_words=True,
	multiple=True
)