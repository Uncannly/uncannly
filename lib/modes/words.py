import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.present import Present
from lib.type_conversion import string_to_array
from data.load_data import load_scores

class Words:
	@staticmethod
	def get(
		interface, 
		return_count, 
		random_selection, 
		scoring_method, 
		score_threshold,
		unweighted, 
		unstressed,
		exclude_real
	):
		most_probable_words = load_scores(unstressed, unweighted, scoring_method)
		sorted_most_probable_words = sorted(most_probable_words, key=lambda x: -x[1])

		if random_selection:
			word_tuples = sorted_most_probable_words[0:int(random_selection)]
			selector = api_select_random if interface == 'api' else bin_select_random
		else:
			word_tuples = sorted_most_probable_words
			selector = api_select_top if interface == 'api' else bin_select_top

		words = []
		for index, (word, score) in enumerate(word_tuples):
			if score < score_threshold:
				break
			else:
				words.append(word)
		
		return selector(words, return_count, unstressed, exclude_real)

def bin_select_top(words, return_count, unstressed, exclude_real):
	i = 0
	for _ in xrange(return_count):
		if i == len(words):
			sys.stdout.write(
				'Fewer words met criteria than the specified return count.\n'
			)
			break
		presented = False
		while presented == False:
			presented = Present.for_terminal(words[i], unstressed, exclude_real)
			i += 1

def bin_select_random(words, return_count, unstressed, exclude_real):
	for _ in xrange(return_count):
		while Present.for_terminal(random.choice(words), unstressed, exclude_real) == False:
			pass

def api_select_top(words, return_count, unstressed, exclude_real):
	output = []
	i = 0
	no_words_returned = True
	while len(output) < return_count:
		if i == len(words):
			output.append('Fewer words met criteria than the specified return count.')
			break
		arrayified_word = string_to_array(words[i])
		i += 1
		result = Present.for_web(arrayified_word, unstressed, exclude_real)
		if result:
			no_words_returned = False
			output.append(result) 	

	if no_words_returned:
		output = ['No words met criteria.']

	return output

def api_select_random(words, return_count, unstressed, exclude_real):
	output = []
	while len(output) < return_count:
		arrayified_word = string_to_array(random.choice(words))
		result = Present.for_web(arrayified_word, unstressed, exclude_real)
		if result:
			output.append(result) 

	if len(output) == 0:
		output = ['No words met criteria.']

	return output