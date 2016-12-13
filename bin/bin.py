import argparse, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.mode import get_by_mode

def bin(mode):
	parser = argparse.ArgumentParser(
		description='Get the most likely yet missing English words.'
	)

	parser.add_argument(
		'--return-count', '-c', 
		type=int, default=45, 
		help='How many words to return at once. (only applies in `words` mode)'
	)
	parser.add_argument(
		'--random-selection', '-r',
		nargs='?', const=1000000, type=int,
		help='From this particularly specified set of most probable words, instead of the absolute topmost probable ones, return a random selection. (only applies in `words` mode)'
	)
	parser.add_argument(
		'--scoring-method', '-m',
		help='The method used to score words by, and filter out the lower scoring ones. Four methods exist in a 2x2 matrix relationship: integral-product, integral-sum, mean-geometric, mean-arithmetic.'
	)
	parser.add_argument(
		'--score-by-integral-product', '-p',
		action='store_true',
		help='Alias for "--scoring-method=integral-product".'
	)
	parser.add_argument(
		'--score-by-integral-sum', '-s',
		action='store_true',
		help='Alias for "--scoring-method=integral-sum".'
	)
	parser.add_argument(
		'--score-by-mean-geometric', '-g',
		action='store_true',
		help='Alias for "--scoring-method=mean-geometric".'
	)
	parser.add_argument(
		'--score-by-mean-arithmetic', '-a',
		action='store_true',
		help='Alias for "--scoring-method=mean-arithmetic".'
	)
	parser.add_argument(
		'--score-threshold', '-t',
		type=float,
		help='When specified, will not return words with scores (according to the current scoring method) lower than this threshold.'
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
	get_by_mode(mode=mode, interface='bin', args=vars(args))