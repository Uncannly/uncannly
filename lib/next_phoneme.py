import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.secondary_data_io import load

cumulative_distributions = load('cumulative_distributions')

def next_phoneme(phoneme, random_number):
	return next(step['next_phoneme']
		for step in cumulative_distributions[phoneme]
		if step['accumulated_probability'] >= random_number
	)