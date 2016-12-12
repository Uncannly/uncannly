import os, sys, argparse
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.words import Words

parser = argparse.ArgumentParser(
	description='Get the most likely yet missing English words.'
)
parser.add_argument(
	'--return-count', '-c', 
	type=int, default=45, 
	help='How many words to return at once.'
)
parser.add_argument(
	'--mean-arithmetic', '-a',
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

Words.get(
	interface="bin",
	return_count=args.return_count, 
	scoring_method='mean_arithmetic' if args.mean_arithmetic else 'integral_product', 
	weighting='unweighted' if args.unweighted else 'weighted',
	random_selection=args.random_selection,
	exclude_real=args.exclude_real
)