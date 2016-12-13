import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.mode import get_by_mode

def api(mode, args):
	return get_by_mode(mode=mode, interface='api', args=args)