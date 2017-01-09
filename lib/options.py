OPTION_VALUES = {
    'stressing': ('unstressed', 'stressed'),
    'weighting': ('unweighted', 'weighted'),
    'positioning': ('ignore_position', 'use_position'),
    'length_consideration': ('ignore_length', 'use_length')
}

def option_value_boolean_to_string(option, boolean):
    index = 0 if boolean else 1
    return OPTION_VALUES[option][index]

def option_value_string_to_boolean(value):
    for values in OPTION_VALUES.itervalues():
        if value == values[0]:
            return True
        elif value == values[1]:
            return False

SCORING_METHODS = {
    'integral_product': (False, False),
    'integral_sum': (False, True),
    'mean_geometric': (True, False),
    'mean_arithmetic': (True, True),
}

TOO_FEW_MESSAGE = 'Fewer words met criteria than the specified return count.\n'
NO_WORDS_MESSAGE = 'No words met criteria.\n'

POOL_DEFAULT = 25
POOL_MAX = 500

MAX_FAILS = 1000000

MAX_WORD_LENGTH = 20
