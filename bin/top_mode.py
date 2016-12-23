import json, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.cli import cli
cli('top')