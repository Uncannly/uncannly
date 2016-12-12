import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.words import Words

def get(return_count,	mean_arithmetic, random_selection, unweighted, exclude_real):
	return Words.get(
		interface='api', 
		return_count=int(return_count) if return_count else 45,	
		filtering='mean_arithmetic' if mean_arithmetic != None else 'integral_product', 
		random_selection=random_selection != None, 
		weighting='unweighted' if unweighted != None else 'weighted', 
		exclude_real=exclude_real != None
	)