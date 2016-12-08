import random, time, os, sys, argparse
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import random_word

parser = argparse.ArgumentParser(
	description='Get the most likely yet missing English words.'
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

random_word.get("bin", unweighted=args.unweighted, exclude_real=args.exclude_real)