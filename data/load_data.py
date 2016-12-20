import json

from database import Database

def load_words(unstressed):
	return Database.fetch("select word, {} from words;".format(
			'pronunciation_unstressed' if unstressed else 'pronunciation'
		))

def load_scores(scoring_method, unweighted, unstressed):
	if scoring_method == 'integral_product':
		method_mean = False
		method_addition = False
	elif scoring_method == 'integral_sum':
		method_mean = False
		method_addition = True
	elif scoring_method == 'mean_geometric':
		method_mean = True
		method_addition = False
	elif scoring_method == 'mean_arithmetic':
		method_mean = True
		method_addition = True

	
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