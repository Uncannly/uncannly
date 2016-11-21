import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.terminal import sorted_most_probable_words

sorted_most_probable_words.share('continued_product', 'unweighted')