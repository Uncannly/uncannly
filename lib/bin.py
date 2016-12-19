import argparse, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from mode import get_by_mode
from readme import readme

def bin(mode):
	parser = argparse.ArgumentParser(
		description='Get the most likely yet missing English words.'
	)

	parser.add_argument(
		'--return-count', '-c', 
		type=int, default=45, 
		help=readme.get('return_count')
	)
	parser.add_argument(
		'--random-selection', '-r',
		nargs='?', const=10000, type=int,
		help=readme.get('random_selection')
	)
	parser.add_argument(
		'--scoring-method', '-m',
		help=readme.get('scoring_method')
	)
	parser.add_argument(
		'--score-by-integral-product', '-p',
		action='store_true',
		help=readme.get('score_by_integral_product')
	)
	parser.add_argument(
		'--score-by-integral-sum', '-s',
		action='store_true',
		help=readme.get('score_by_integral_sum')
	)
	parser.add_argument(
		'--score-by-mean-geometric', '-g',
		action='store_true',
		help=readme.get('score_by_mean_geometric')
	)
	parser.add_argument(
		'--score-by-mean-arithmetic', '-a',
		action='store_true',
		help=readme.get('score_by_mean_arithmetic')
	)
	parser.add_argument(
		'--score-threshold', '-t',
		type=float,
		help=readme.get('score_threshold')
	)
	parser.add_argument(
		'--unweighted', '-u',
		action='store_true',
		help=readme.get('unweighted')
	)
	parser.add_argument(
		'--ignore-stress', '-i',
		action='store_true',
		help=readme.get('ignore_stress')
	)
	parser.add_argument(
		'--exclude-real', '-x', 
		action='store_true',
		help=readme.get('exclude_real')
	)

	args = parser.parse_args()
	get_by_mode(mode=mode, interface='bin', args=vars(args))