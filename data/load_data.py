import json

from database import fetch

def load_words(stressless):
	return fetch("select word, {} from words;".format(
			'pronunciation_stressless' if stressless else 'pronunciation'
		))

def load_scores(stressless, unweighted, scoring_method):
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
		stressless = {} and unweighted = {} \
		and method_mean = {} and method_addition = {};".format(
			stressless, unweighted, method_mean, method_addition
		)
	
	return fetch(sql)

def load_phonemes(stressless, unweighted):
	next_phonemes = 'next_phonemes_unweighted' if unweighted else 'next_phonemes'
	sql = "select phoneme, {} from phonemes where stressless = {};".format(
		next_phonemes, stressless
	)
	results = fetch(sql)

	output = {}
	for phoneme, next_phonemes in results:
		output[phoneme] = json.loads(next_phonemes)

	return output