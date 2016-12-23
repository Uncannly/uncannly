import argparse, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from lib.mode import get_by_mode
from lib.readme import readme
from lib.options import pool_default

def bin(mode):
  parser = argparse.ArgumentParser(
      description='Get the most likely yet missing English words.'
  )

  parser.add_argument(
      '--pool', '-p',
      type=int, default=pool_default,
      help=readme.get('pool')
  )
  parser.add_argument(
      '--selection', '-s',
      nargs='?', const=pool_default, type=int,
      help=readme.get('selection')
  )
  parser.add_argument(
      '--top-selection', '-t',
      nargs='?', const=pool_default, type=int,
      help='Alias for `selection` when in random mode.'
  )
  parser.add_argument(
      '--random-selection', '-w',
      nargs='?', const=pool_default, type=int,
      help='Alias for `selection` when in top mode.'
  )
  parser.add_argument(
      '--scoring-method', '-r',
      help=readme.get('scoring_method')
  )
  parser.add_argument(
      '--score-by-integral-product', '-m',
      action='store_true',
      help=readme.get('score_by_integral_product')
  )
  parser.add_argument(
      '--score-by-integral-sum', '-a',
      action='store_true',
      help=readme.get('score_by_integral_sum')
  )
  parser.add_argument(
      '--score-by-mean-geometric', '-g',
      action='store_true',
      help=readme.get('score_by_mean_geometric')
  )
  parser.add_argument(
      '--score-by-mean-arithmetic', '-v',
      action='store_true',
      help=readme.get('score_by_mean_arithmetic')
  )
  parser.add_argument(
      '--score-threshold', '-c',
      type=float,
      help=readme.get('score_threshold')
  )
  parser.add_argument(
      '--unweighted', '-u',
      action='store_true',
      help=readme.get('unweighted')
  )
  parser.add_argument(
      '--unstressed', '-i',
      action='store_true',
      help=readme.get('unstressed')
  )
  parser.add_argument(
      '--exclude-real', '-x',
      action='store_true',
      help=readme.get('exclude_real')
  )

  args = parser.parse_args()
  get_by_mode(mode=mode, interface='bin', args=vars(args))