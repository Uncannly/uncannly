readme = {
	'return_count': 'How many words to return at once. \
		(only applies in `words` mode)',
	'random_selection': 'From this particularly specified set \
		of most probable words, instead of the absolute topmost probable ones, \
		return a random selection. (only applies in `words` mode)',
	'scoring_method': 'The method used to score words by, and filter out \
		the lower scoring ones. Four methods exist in a 2x2 matrix relationship: \
		integral-product, integral-sum, mean-geometric, mean-arithmetic.',
	'score_by_integral_product': 'Alias for "--scoring-method=integral-product".',
	'score_by_integral_sum': 'Alias for "--scoring-method=integral-sum".',
	'score_by_mean_geometric': 'Alias for "--scoring-method=mean-geometric".',
	'score_by_mean_arithmetic': 'Alias for "--scoring-method=mean-arithmetic".',
	'score_threshold': 'When specified, will not return words with scores \
		(according to the current scoring method) lower than this threshold.',
	'unweighted': 'Do not weight probabilities by frequency of words in the corpus.',
	'exclude_real': 'Do not include words probable by pronunciation that do exist.'
}