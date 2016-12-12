import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.words import Words
from lib.case_conversion import kebab_to_snake

def get(return_count,	scoring_method, random_selection, unweighted, exclude_real):
	if scoring_method == None:
		scoring_method = 'integral_product'
	else:
		scoring_method = kebab_to_snake(scoring_method)

	return Words.get(
		interface='api', 
		return_count=int(return_count) if return_count else 45,	
		scoring_method=scoring_method, 
		random_selection=random_selection != None, 
		weighting='unweighted' if unweighted != None else 'weighted', 
		exclude_real=exclude_real != None
	)