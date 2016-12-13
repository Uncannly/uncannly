import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.random_word import RandomWord
from lib.case_conversion import kebab_to_snake

def get(
	return_count,	
	random_selection, 
	unweighted, 
	scoring_method, 
  score_by_integral_product, 
  score_by_integral_sum, 
  score_by_mean_geometric, 
  score_by_mean_arithmetic, 
  score_threshold,
	exclude_real):

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

	return RandomWord.get(
		interface="api", 
		scoring_method=scoring_method, 
		score_threshold=float(score_threshold) if score_threshold else None,
		unweighted=unweighted != None, 
		exclude_real=exclude_real != None
	)