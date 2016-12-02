import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.present import Present
from lib.secondary_data_io import load

def flagged(single_char_flag, full_word_flag):
	return single_char_flag in sys.argv or full_word_flag in sys.argv

def share(return_count, selection, threshold, frequency_weighting, include_real_words):
		most_probable_words = load(
			'most_probable_words_by_{}_{}'.format(threshold, frequency_weighting)
		)

		print 'total generated most probable words:', len(most_probable_words)

		if selection == 'top':
			top_selection(most_probable_words, return_count)
		elif selection == 'random':
			random_selection(most_probable_words, return_count)

def top_selection(most_probable_words, return_count):
	words = sorted(most_probable_words,	key=most_probable_words.get, reverse=True)
	for i in range(0, return_count):
		Present.for_terminal(words[i], include_real_words)
		

def random_selection(most_probable_words, return_count):
	words = most_probable_words.keys()
	for i in range(0, return_count):
		Present.for_terminal(random.choice(words), include_real_words) 
		

return_count = int(sys.argv[1])

if flagged('-r', '--random'):
	selection = 'random'
else:
	selection = 'top'

if flagged('-a', '--by-averaging'):
	threshold = 'averaging'
elif flagged('-c', '--by-continued-product'):
	threshold = 'continued_product'
else:
	print 'You must specify a threshold (either by averaging or by continued product).'

if flagged('-u', '--unweighted'):
	frequency_weighting = 'unweighted'
else:
	frequency_weighting = 'weighted'

if flagged('-x', '--exclude-real-words'):
	include_real_words = False
else:
	include_real_words = True

share(return_count, selection, threshold, frequency_weighting, include_real_words)