import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.secondary_data_io import load

cumulative_distributions_weighted = load('cumulative_distributions')
cumulative_distributions_unweighted = load('cumulative_distributions_unweighted')

def next_phoneme(phoneme, random_number, weighted_by_frequency):
	if weighted_by_frequency == True:
		cumulative_distributions = cumulative_distributions_weighted
	else:
		cumulative_distributions = cumulative_distributions_unweighted
	
	return next(step['next_phoneme']
		for step in cumulative_distributions[phoneme]
		if step['accumulated_probability'] >= random_number
	)