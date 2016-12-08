import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.present import Present
from lib.secondary_data_io import load
from lib.type_conversion import string_to_array, kebab_to_snake

class Words:
	@staticmethod
	def get(
		interface, 
		return_count, 
		filtering, 
		weighting, 
		random_selection, 
		exclude_real
	):
		most_probable_words = load(
			'most_probable_words_by_{}_{}'.format(filtering, weighting)
		)

		if random_selection:
			words = most_probable_words.keys()
		else:
			words = sorted(
				most_probable_words,
				key=most_probable_words.get,
				reverse=True
			)

		if interface == 'api':
			selector = api_select_random if random_selection else api_select_top
		elif interface == 'bin':
			selector = bin_select_random if random_selection else bin_select_top
			sys.stdout.write(
				'total generated most probable words: ' + len(most_probable_words) + '\n'
			)
		
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