import json, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.bin import bin
bin('random')