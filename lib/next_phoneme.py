import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.secondary_data_io import load

weighted_distributions = load('cumulative_distributions')
unweighted_distributions = load('cumulative_distributions_unweighted')

def next_phoneme(phoneme, random_number, unweighted):
	distributions = unweighted_distributions if unweighted else weighted_distributions
	
	return next(step['next_phoneme']
		for step in distributions[phoneme]
		if step['accumulated_probability'] >= random_number
	)