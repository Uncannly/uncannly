import json

from database import Database

scoring_method_breakdown = {
	'integral_product': (False, False),
	'integral_sum': (False, True),
	'mean_geometric': (True, False),
	'mean_arithmetic': (True, True),
}

def load_words():
	return Database.fetch("select * from words;")

def load_scores(scoring_method, unweighted, unstressed):
	method_mean, method_addition = scoring_method_breakdown[scoring_method]

	sql = "select word, score from scores where \
		unweighted = {} and unstressed = {} \
		and method_mean = {} and method_addition = {};".format(
			unweighted, unstressed, method_mean, method_addition
		)
	
	return Database.fetch(sql)

def load_phonemes(unweighted, unstressed):
	next_phonemes = 'next_phonemes_unweighted' if unweighted else 'next_phonemes'
	sql = "select phoneme, {} from phonemes where unstressed = {};".format(
		next_phonemes, unstressed
	)
	results = Database.fetch(sql)

	output = {}
	for phoneme, next_phonemes in results:
		output[phoneme] = json.loads(next_phonemes)

	return output