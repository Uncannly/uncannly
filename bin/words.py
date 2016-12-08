import random, os, sys, argparse
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.present import Present
from lib.secondary_data_io import load

def share(return_count, filtering, weighting, random_selection, exclude_real):
	most_probable_words = load(
		'most_probable_words_by_{}_{}'.format(filtering, weighting)
	)

	print 'total generated most probable words:', len(most_probable_words)

	selector = select_random if random_selection else select_top
	selector(most_probable_words, return_count, exclude_real)

def select_top(most_probable_words, return_count, exclude_real):
	words = sorted(most_probable_words,	key=most_probable_words.get, reverse=True)
	i = 0
	for _ in xrange(return_count):
		if i == len(words):
			print 'Fewer words met criteria than the specified return count.'
			break
		presented = False
		while presented == False:
			presented = Present.for_terminal(words[i], exclude_real)
			i += 1

def select_random(most_probable_words, return_count, exclude_real):
	words = most_probable_words.keys()
	for _ in xrange(return_count):
		while Present.for_terminal(random.choice(words), exclude_real) == False:
			pass


parser = argparse.ArgumentParser(
	description='Get the most likely yet missing English words.'
)
parser.add_argument(
	'--return-count', '-c', 
	type=int, default=45, 
	help='How many words to return at once.'
)
parser.add_argument(
	'--averaging', '-a',
	action='store_true',
	help='Use the list of most likely words which was created by cutting off words when they passed a threshold based on averaging the probabilities of phonemes following each other (instead of taking the continued product of these probabilities, which is the default).'
)
parser.add_argument(
	'--random-selection', '-r',
	action='store_true',
	help='From this particularly specified set of most probable words, instead of the absolute topmost probable ones, return a random selection.'
)
parser.add_argument(
	'--unweighted', '-u',
	action='store_true',
	help='Do not weight probabilities by frequency of words in the corpus.'
)
parser.add_argument(
	'--exclude-real', '-x', 
	action='store_true',
	help='Do not include words probable by pronunciation that do exist.'
)

args = parser.parse_args()

share(
	return_count=args.return_count, 
	filtering='averaging' if args.averaging else 'continued_product', 
	weighting='unweighted' if args.unweighted else 'weighted',
	random_selection=args.random_selection,
	exclude_real=args.exclude_real
)