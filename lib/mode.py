from words import Words
from random_word import RandomWord
from case_conversion import kebab_to_snake

def get_by_mode(mode, interface, args):

	if args['return_count']:
		args['return_count'] = int(args['return_count'])
	else:
		args['return_count'] = 45

	if args.get('score_by_mean_arithmetic'):
		args['scoring_method'] = 'mean_arithmetic'
	if args.get('score_by_mean_geometric'):
		args['scoring_method'] = 'mean_geometric'
	if args.get('score_by_integral_sum'):
		args['scoring_method'] = 'integral_sum'
	if args.get('score_by_integral_product'):
		args['scoring_method'] = 'integral_product'

	if args.get('scoring_method') == None:
		args['scoring_method'] = 'integral_product'
	else:
		args['scoring_method'] = kebab_to_snake(args['scoring_method'])

	if args['score_threshold']:
		args['score_threshold'] = float(args['score_threshold'])
	else:
		args['score_threshold'] = None

	getter = Words if mode == 'words' else RandomWord
	return getter.get(
		interface=interface,
		return_count=args['return_count'], 
		random_selection=args['random_selection'],
		scoring_method=args['scoring_method'],
		score_threshold=args['score_threshold'],
		unweighted=args['unweighted'],
		exclude_real=args['exclude_real']
	)