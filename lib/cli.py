import argparse
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from lib.mode import get_by_mode
from lib.readme import README
from lib.options import POOL_DEFAULT

def cli(mode):
    parser = argparse.ArgumentParser(
        description='Get the most likely yet missing English words.'
    )

    parser.add_argument(
        '--pool', '-p',
        type=int, default=POOL_DEFAULT,
        help=README.get('pool')
    )
    parser.add_argument(
        '--selection', '-s',
        nargs='?', const=POOL_DEFAULT, type=int,
        help=README.get('selection')
    )
    parser.add_argument(
        '--top-selection', '-ts',
        nargs='?', const=POOL_DEFAULT, type=int,
        help='Alias for `selection` when in random mode.'
    )
    parser.add_argument(
        '--random-selection', '-rs',
        nargs='?', const=POOL_DEFAULT, type=int,
        help='Alias for `selection` when in top mode.'
    )
    parser.add_argument(
        '--scoring-method', '-sm',
        help=README.get('scoring_method')
    )
    parser.add_argument(
        '--score-by-integral-product', '-ip',
        action='store_true',
        help=README.get('score_by_integral_product')
    )
    parser.add_argument(
        '--score-by-integral-sum', '-is',
        action='store_true',
        help=README.get('score_by_integral_sum')
    )
    parser.add_argument(
        '--score-by-mean-geometric', '-mg',
        action='store_true',
        help=README.get('score_by_mean_geometric')
    )
    parser.add_argument(
        '--score-by-mean-arithmetic', '-ma',
        action='store_true',
        help=README.get('score_by_mean_arithmetic')
    )
    parser.add_argument(
        '--score-threshold', '-st',
        type=float,
        help=README.get('score_threshold')
    )
    parser.add_argument(
        '--unweighted', '-xw',
        action='store_true',
        help=README.get('unweighted')
    )
    parser.add_argument(
        '--unstressed', '-xs',
        action='store_true',
        help=README.get('unstressed')
    )
    parser.add_argument(
        '--exclude-real', '-xr',
        action='store_true',
        help=README.get('exclude_real')
    )
    parser.add_argument(
        '--ignore-position', '-xp',
        action='store_true',
        help=README.get('ignore_position')
    )
    parser.add_argument(
        '--ignore-length', '-xl',
        action='store_true',
        help=README.get('ignore_length')
    )
    parser.add_argument(
        '--min-length', '-mn', type=int,
        help=README.get('min_length')
    )
    parser.add_argument(
        '--max-length', '-mx', type=int,
        help=README.get('max_length')
    )

    args = parser.parse_args()
    get_by_mode(mode=mode, interface='cli', args=vars(args))
