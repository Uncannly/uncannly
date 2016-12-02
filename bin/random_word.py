import random, time, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import random_word

random_word.get("bin", weighted_by_frequency=True, include_real_words=True)