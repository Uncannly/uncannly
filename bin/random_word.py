import random, time, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import random_word
from lib.flagged import flagged

if flagged('-u', '--unweighted'):
	weighted_by_frequency = False
else:
	weighted_by_frequency = True

if flagged('-x', '--exclude-real-words'):
	include_real_words = False
else:
	include_real_words = True

random_word.get("bin", weighted_by_frequency, include_real_words)