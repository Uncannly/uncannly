import sys
from lib.options import POOL_DEFAULT

# pylint: disable=too-few-public-methods,no-self-use

class TopModeSyllables(object):
    def __init__(self, options):
        self.interface = options.get('interface', 'api')
        self.pool = options.get('pool', POOL_DEFAULT)
        self.selection = options.get('selection')
        self.scoring_method = options.get('scoring_method')
        self.score_threshold = options.get('score_threshold')
        self.unweighted = options.get('unweighted')
        self.unstressed = options.get('unstressed')
        self.exclude_real = options.get('exclude_real')
        self.ignore_position = options.get('ignore_position')
        self.ignore_length = options.get('ignore_length')
        self.min_length = options.get('min_length')
        self.max_length = options.get('max_length')
        self.ignore_syllables = options.get('ignore_syllables')

    def get(self):
        message = 'Not yet implemented. Please ignore syllables.'
        sys.stdout.write(message + '\n')
        return [(message, 0)]
# pylint: enable=too-few-public-methods,no-self-use
