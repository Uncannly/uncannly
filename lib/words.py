import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from present import Present
from secondary_data_io import load
from type_conversion import string_to_array

class Words:
	@staticmethod
	def get(
		interface, 
		return_count, 
		scoring_method, 
		weighting, 
		random_selection, 
		exclude_real
	):
		most_probable_words = load(
			'most_probable_words_by_{}_{}'.format(scoring_method, weighting)
		)

		if random_selection:
			words = most_probable_words[0:int(random_selection)]
			selector = api_select_random if interface == 'api' else bin_select_random
		else:
			words = most_probable_words
			selector = api_select_top if interface == 'api' else bin_select_top
		
		return selector(words, return_count, exclude_real)

def bin_select_top(words, return_count, exclude_real):
	i = 0
	for _ in xrange(return_count):
		if i == len(words):
			sys.stdout.write(
				'Fewer words met criteria than the specified return count.\n'
			)
			break
		presented = False
		while presented == False:
			presented = Present.for_terminal(words[i], exclude_real)
			i += 1

def bin_select_random(words, return_count, exclude_real):
	for _ in xrange(return_count):
		while Present.for_terminal(random.choice(words), exclude_real) == False:
			pass

def api_select_top(words, return_count, exclude_real):
	output = []
	i = 0
	while len(output) < return_count:
		if i == len(words):
			sys.stdout.write(
				'Fewer words met criteria than the specified return count.\n'
			)
			break
		arrayified_word = string_to_array(words[i])
		i += 1
		result = Present.for_web(arrayified_word, exclude_real)
		if result:
			output.append(result) 	
	return output

def api_select_random(words, return_count, exclude_real):
	output = []
	while len(output) < return_count:
		arrayified_word = string_to_array(random.choice(words))
		result = Present.for_web(arrayified_word, exclude_real)
		if result:
			output.append(result) 
	return output