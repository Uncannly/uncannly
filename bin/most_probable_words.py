import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.terminal import random_most_probable_words, sorted_most_probable_words

def flagged(short, long):
	if short in sys.argv or long in sys.argv:
		return True
	else:
		return False

if flagged('-s', '--sorted'):
	sharer = sorted_most_probable_words
elif flagged('-r', '--random'):
	sharer = random_most_probable_words
else:
	print 'You must specify either random or sorted.'

if flagged('-a', '--by-averaging'):
	filter = 'averaging'
elif flagged('-c', '--by-continued-product'):
	filter = 'continued_product'
else:
	print 'You must specify a filter (either by averaging or by continued product).'

if flagged('-u', '--unweighted'):
	frequency_weighting = 'unweighted'
else:
	frequency_weighting = 'weighted'

if flagged('-x', '--exclude-real-words'):
	include_real_words = False
else:
	include_real_words = True

sharer.share(filter, frequency_weighting, include_real_words)