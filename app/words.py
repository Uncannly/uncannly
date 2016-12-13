import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.words import Words
from lib.case_conversion import kebab_to_snake

def get(
	return_count,	
	random_selection, 
	scoring_method, 
	score_by_integral_product,
	score_by_integral_sum,
	score_by_mean_geometric,
	score_by_mean_arithmetic,
	score_threshold,
	unweighted, 
	exclude_real):

	if random_selection == '':
		random_selection = 1000000

	if score_by_mean_arithmetic:
		scoring_method = 'mean_arithmetic'
	if score_by_mean_geometric:
		scoring_method = 'mean_geometric'
	if score_by_integral_sum:
		scoring_method = 'integral_sum'
	if score_by_integral_product:
		scoring_method = 'integral_product'

	if scoring_method == None:
		scoring_method = 'integral_product'
	else:
		scoring_method = kebab_to_snake(scoring_method)

	return Words.get(
		interface='api', 
		return_count=int(return_count) if return_count else 45,	
		random_selection=random_selection, 
		scoring_method=scoring_method, 
		score_threshold=float(score_threshold) if score_threshold else None,
		weighting='unweighted' if unweighted != None else 'weighted', 
		exclude_real=exclude_real != None
	)