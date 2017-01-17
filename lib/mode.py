from lib.modes.top_mode import TopMode
from lib.modes.random_mode_phonemes import RandomModePhonemes
from lib.modes.random_mode_syllables import RandomModeSyllables
from lib.conversion import kebab_to_snake
from lib.options import SCORING_METHODS, POOL_DEFAULT

def get_by_mode(mode, interface, args):
    get_args = {'selection': None, 'scoring_method': 'integral_product', 'interface': interface}

    get_args['pool'] = int(args['pool']) if args['pool'] else POOL_DEFAULT

    if args['selection'] is not None:
        get_args['selection'] = args['pool'] if args['selection'] == '' \
            else int(args['selection'])

    if args['top_selection'] and mode == 'random':
        get_args['selection'] = int(args['top_selection'])
    if args['random_selection'] and mode == 'top':
        get_args['selection'] = int(args['random_selection'])

    if args['scoring_method']:
        get_args['scoring_method'] = kebab_to_snake(args['scoring_method'])
    else:
        for method in SCORING_METHODS:
            if args.get('score_by_{}'.format(method)):
                get_args['scoring_method'] = method

    get_args['score_threshold'] = float(args['score_threshold']) \
        if args['score_threshold'] else None

    get_args['unweighted'] = args['unweighted'] or args['unweighted'] == ''
    get_args['unstressed'] = args['unstressed'] or args['unstressed'] == ''
    get_args['exclude_real'] = args['exclude_real'] or args['exclude_real'] == ''
    get_args['ignore_position'] = args['ignore_position'] or args['ignore_position'] == ''
    get_args['ignore_length'] = args['ignore_length'] or args['ignore_length'] == ''
    get_args['ignore_syllables'] = args['ignore_syllables'] or args['ignore_syllables'] == ''

    get_args['min_length'] = int(args['min_length']) if args['min_length'] else None
    get_args['max_length'] = int(args['max_length']) if args['max_length'] else None

    if args['ignore_syllables'] or args['ignore_syllables'] == '':
        getter = TopMode if mode == 'top' else RandomModePhonemes
    else:
        getter = TopMode if mode == 'top' else RandomModeSyllables
    return getter(get_args).get()
