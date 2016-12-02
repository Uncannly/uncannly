import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.terminal import random_most_probable_words, sorted_most_probable_words

# -u --unweighted 
# -x --exclude-real-words  STILL HAVENT DONE THIS ONE YET
# -a --by-averaging            
# -c --by-continued-product   
# -s --sorted
# -r --random

if '-s' in sys.argv or '--sorted' in sys.argv:
	sharer = sorted_most_probable_words
elif '-r' in sys.argv or '--random' in sys.argv:
	sharer = random_most_probable_words
else:
	print 'You must specify either random or sorted.'

if '-a' in sys.argv or '--by-averaging' in sys.argv:
	filter = 'averaging'
elif '-c' in sys.argv or '--by-continued-product' in sys.argv:
	filter = 'continued_product'
else:
	print 'You must specify a filter (either by averaging or by continued product).'

if '-u' in sys.argv or '--unweighted' in sys.argv:
	frequency_weighting = 'unweighted'
else:
	frequency_weighting = 'weighted'

if '-x' in sys.argv or '--exclude-real-words' in sys.argv:
	include_real_words = False
else:
	include_real_words = True

sharer.share(filter, frequency_weighting, include_real_words)