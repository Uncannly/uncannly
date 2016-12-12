import random, time, os, sys, argparse
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.random_word import RandomWord
from lib.case_conversion import kebab_to_snake

parser = argparse.ArgumentParser(
	description='Get the most likely yet missing English words.'
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

if args.score_by_mean_arithmetic:
	args.scoring_method = 'mean_arithmetic'
if args.score_by_mean_geometric:
	args.scoring_method = 'mean_geometric'
if args.score_by_integral_sum:
	args.scoring_method = 'integral_sum'
if args.score_by_integral_product:
	args.scoring_method = 'integral_product'

if args.scoring_method == None:
	args.scoring_method = 'integral_product'
else:
	args.scoring_method = kebab_to_snake(args.scoring_method)

RandomWord.get(
	interface="bin", 
	scoring_method=args.scoring_method,
	score_threshold=args.score_threshold,
	unweighted=args.unweighted, 
	exclude_real=args.exclude_real
)