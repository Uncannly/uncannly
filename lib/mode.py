from modes.top_mode import TopMode
from modes.random_mode import RandomMode
from case_conversion import kebab_to_snake

def get_by_mode(mode, interface, args):

	if args['pool']:
		args['pool'] = int(args['pool'])
	else:
		args['pool'] = 45

	if args['selection'] is not None:
		if args['selection'] == '':
			args['selection'] = args['pool']
		else:
			args['selection'] = int(args['selection'])

	if args['top_selection'] and mode == 'random':
		args['selection'] = int(args['top_selection'])
	if args['random_selection'] and mode == 'top':
		args['selection'] = int(args['random_selection'])

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

	if args['unweighted'] == None:
		args['unweighted'] = False
	elif args['unweighted'] != False:
		args['unweighted'] = True

	if args['unstressed'] == None:
		args['unstressed'] = False
	elif args['unstressed'] != False:
		args['unstressed'] = True

	if args['exclude_real'] == None:
		args['exclude_real'] = False
	elif args['exclude_real'] != False:
		args['exclude_real'] = True

	getter = TopMode if mode == 'top' else RandomMode
	return getter.get(
		interface=interface,
		pool=args['pool'], 
		selection=args['selection'],
		scoring_method=args['scoring_method'],
		score_threshold=args['score_threshold'],
		unweighted=args['unweighted'],
		unstressed=args['unstressed'],
		exclude_real=args['exclude_real']
	)