readme = {
	'pool': 'How many words to gather by the chosen mode.',
	'selection': 'When enabled, use the other mode to select within the pool. \
		When no value is provided, select all. For example, in top mode, enable \
		selection with no value just to throw away the ordering of these top words. \
		You can add a selection value smaller or equal to the pool to lock down \
		how many of them are returned, then increase the pool to increase the \
		proportion of less probable words within that selection count. \
		In random mode, enable selection with no value to sort the randomly \
		generated words by probability. You can add a selection value smaller or \
		eqaul to the pool to lock down how many of them are returned, \
		then increase the pool to increase the proportion of more probable words \
		within that selection count.',
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
	'unstressed': 'Ignore stress levels of vowels.',
	'exclude_real': 'Do not include words probable by pronunciation that do exist.'
}

