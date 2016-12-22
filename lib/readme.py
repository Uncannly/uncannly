readme = {
	'pool': 'How many words to gather by the chosen mode.',

	'selection': (
		'When enabled, use the other mode to select within the pool. \n\n'
		'When enabled and no value is provided, use the other mode, but select all '
		'(read: in `top` mode, scramble and introduce repeats; '
		'in `random` mode, sort). \n\n'
		'In top mode, you can add a selection value smaller or equal to the pool to '
		'lock down how many of them are returned, then increase the pool to increase '
		'the proportion of less probable words within that selection count. \n\n'
		'In random mode, take the same action to increase the proportion of *more* '
		'probable words within that selection count, by generating more and more '
		'random words that might be more probable than ones you\'d already generated. \n\n'
		'The selection count cannot be larger than the pool. \n\n'
		'Default: disabled (when enabled, defaults to 10).'
	),

	'random_selection': (
		'Randomly select within the top pool. \n\n'
		'When enabled but no value is provided, the effect is to scramble and '
		'likely lose some to repetition. '
		'Add a selection value to lock down a return count, '
		'then increase the pool to increase the proportion of less probable words. \n\n'
		'The selection count cannot be larger than the pool. \n\n'
		'Default: disabled (when enabled, defaults to 10).'
	),

	'top_selection': (
		'Select the topmost likely words from the randomly generated pool. \n\n'
		'When enabled but no value is provided, select all (i.e. sort them). \n\n'
		'Add a selection value to lock down a return count, '
		'then increase the pool to increase the proportion of more probable words. \n\n'
		'The selection count cannot be larger than the pool. \n\n'
		'Default: disabled (when enabled, defaults to 10).'
	),

	'scoring_method': (
		'The method used to score words by, and filter out the lower scoring ones. \n\n'
		'Four methods exist in a 2x2 matrix relationship: '
		'integral-product, integral-sum, mean-geometric, mean-arithmetic.'
	),

	'score_by_integral_product': 'Alias for "--scoring-method=integral-product".',
	'score_by_integral_sum': 'Alias for "--scoring-method=integral-sum".',
	'score_by_mean_geometric': 'Alias for "--scoring-method=mean-geometric".',
	'score_by_mean_arithmetic': 'Alias for "--scoring-method=mean-arithmetic".',

	'score_threshold': (
		'When specified, will not return words with scores (according to the '
		'current scoring method) lower than this threshold.'
	),

	'unweighted': 'Do not weight probabilities by frequency of words in the corpus.',
	'unstressed': 'Ignore stress levels of vowels.',
	'exclude_real': 'Do not include words probable by pronunciation that do exist.'
}
