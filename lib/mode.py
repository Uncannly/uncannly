from modes.top_mode import TopMode
from modes.random_mode import RandomMode
from case_conversion import kebab_to_snake

def get_by_mode(mode, interface, args):
	get_args = {}

	if args['pool']:
		get_args['pool'] = int(args['pool'])
	else:
		get_args['pool'] = 45

	if args['selection'] is not None:
		if args['selection'] == '':
			get_args['selection'] = args['pool']
		else:
			get_args['selection'] = int(args['selection'])

	if args['top_selection'] and mode == 'random':
		get_args['selection'] = int(args['top_selection'])
	if args['random_selection'] and mode == 'top':
		get_args['selection'] = int(args['random_selection'])

	if not get_args.get('selection'):
		get_args['selection'] = None

	if args.get('score_by_mean_arithmetic'):
		get_args['scoring_method'] = 'mean_arithmetic'
	if args.get('score_by_mean_geometric'):
		get_args['scoring_method'] = 'mean_geometric'
	if args.get('score_by_integral_sum'):
		get_args['scoring_method'] = 'integral_sum'
	if args.get('score_by_integral_product'):
		get_args['scoring_method'] = 'integral_product'

	if args.get('scoring_method') == None:
		get_args['scoring_method'] = 'integral_product'
	else:
		get_args['scoring_method'] = kebab_to_snake(args['scoring_method'])

	if args['score_threshold']:
		get_args['score_threshold'] = float(args['score_threshold'])
	else:
		get_args['score_threshold'] = None

	if args['unweighted'] == None or args['unweighted'] == False:
		get_args['unweighted'] = False
	else:
		get_args['unweighted'] = True

	if args['unstressed'] == None or args['unstressed'] == False:
		get_args['unstressed'] = False
	else:
		get_args['unstressed'] = True

	if args['exclude_real'] == None or args['exclude_real'] == False:
		get_args['exclude_real'] = False
	else:
		get_args['exclude_real'] = True

	print get_args

	getter = TopMode if mode == 'top' else RandomMode
	return getter.get(
		interface=interface,
		**get_args
	)