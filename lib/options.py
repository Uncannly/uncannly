def booleans_to_strings(unstressed, unweighted):
    stressing = 'unstressed' if unstressed else 'stressed'
    weighting = 'unweighted' if unweighted else 'weighted'
    return stressing, weighting

SCORING_METHODS = {
    'integral_product': (False, False),
    'integral_sum': (False, True),
    'mean_geometric': (True, False),
    'mean_arithmetic': (True, True),
}

TOO_FEW_MESSAGE = 'Fewer words met criteria than the specified return count.\n'
NO_WORDS_MESSAGE = 'No words met criteria.\n'

# these are all ~10000, which is more than the 1000 of each
# which we are actually capable of fitting in our free plan cloud database
DEFAULT_LIMITS = {
    'use_length': {
        'use_position': {
            'stressed': {
                'weighted': {
                    'integral_product': 8.1   * 10**-5,  #
                    'integral_sum':     9  * 10**-1, #
                    'mean_geometric':   3.1   * 10**-1, #
                    'mean_arithmetic':  8.5  * 10**-1 #
                },
                'unweighted': {
                    'integral_product': 1.4   * 10**-6, #
                    'integral_sum':     4.85  * 10**-1, #
                    'mean_geometric':   2.5   * 10**-1, #
                    'mean_arithmetic':  5.55  * 10**-1 #
                }
            },
            'unstressed': {
                'weighted': {
                    'integral_product': 1  * 10**-5, #
                    'integral_sum':     9.4   * 10**-1, #
                    'mean_geometric':   3.1   * 10**-1, #
                    'mean_arithmetic':  8.69  * 10**-1 #
                },
                'unweighted': {
                    'integral_product': 3.5   * 10**-5, #
                    'integral_sum':     8.9   * 10**-1,  #
                    'mean_geometric':   9.0   * 10**-1, #
                    'mean_arithmetic':  7.98  * 10**-1  #
                }
            }
        },
        'ignore_position': {
            'stressed': {
                'weighted': {
                    'integral_product': 8.1   * 10**-5,
                    'integral_sum':     9.35  * 10**-1,
                    'mean_geometric':   3.1   * 10**-1,
                    'mean_arithmetic':  6.69  * 10**-1
                },
                'unweighted': {
                    'integral_product': 1.3   * 10**-5,
                    'integral_sum':     9.85  * 10**-1,
                    'mean_geometric':   3.0   * 10**-2,
                    'mean_arithmetic':  5.99  * 10**-1
                }
            },
            'unstressed': {
                'weighted': {
                    'integral_product': 9.97  * 10**-5,
                    'integral_sum':     9.4   * 10**-1,
                    'mean_geometric':   3.1   * 10**-1,
                    'mean_arithmetic':  6.69  * 10**-1
                },
                'unweighted': {
                    'integral_product': 3.5   * 10**-5,
                    'integral_sum':     9.9   * 10**-1,
                    'mean_geometric':   9.0   * 10**-2,
                    'mean_arithmetic':  5.98  * 10**-1
                }
            }
        }
    },
    'ignore_length': {
        'use_position': {
            'stressed': {
                'weighted': {
                    'integral_product': 8.1   * 10**-15,  # 16107
                    'integral_sum':     6.35  * 10**-1, # 0
                    'mean_geometric':   3.1   * 10**-3, # 69
                    'mean_arithmetic':  3.5  * 10**-1 # 228740
                },
                'unweighted': {
                    'integral_product': 1.4   * 10**-16, #24519
                    'integral_sum':     1.85  * 10**-1, #1
                    'mean_geometric':   2.5   * 10**-3, # 8
                    'mean_arithmetic':  2.55  * 10**-1 # 50643
                }
            },
            'unstressed': {
                'weighted': {
                    'integral_product': 1  * 10**-14, # 16205
                    'integral_sum':     6.4   * 10**-1, # 0
                    'mean_geometric':   3.1   * 10**-3, # 71
                    'mean_arithmetic':  3.69  * 10**-1 # 2765
                },
                'unweighted': {
                    'integral_product': 3.5   * 10**-16, # 22507
                    'integral_sum':     5.9   * 10**-1,  # 0
                    'mean_geometric':   9.0   * 10**-3, # 1
                    'mean_arithmetic':  2.98  * 10**-1  # 2
                }
            }
        },
        'ignore_position': {
            'stressed': {
                'weighted': {
                    'integral_product': 8.1   * 10**-16,
                    'integral_sum':     6.35  * 10**-2,
                    'mean_geometric':   3.1   * 10**-4,
                    'mean_arithmetic':  2.69  * 10**-1
                },
                'unweighted': {
                    'integral_product': 1.3   * 10**-17,
                    'integral_sum':     5.85  * 10**-2,
                    'mean_geometric':   3.0   * 10**-5,
                    'mean_arithmetic':  1.99  * 10**-1
                }
            },
            'unstressed': {
                'weighted': {
                    'integral_product': 9.97  * 10**-16,
                    'integral_sum':     6.4   * 10**-2,
                    'mean_geometric':   3.1   * 10**-4,
                    'mean_arithmetic':  2.69  * 10**-1
                },
                'unweighted': {
                    'integral_product': 3.5   * 10**-17,
                    'integral_sum':     5.9   * 10**-2,
                    'mean_geometric':   9.0   * 10**-5,
                    'mean_arithmetic':  1.98  * 10**-1
                }
            }
        }
    }
}

POOL_DEFAULT = 25
POOL_MAX = 1000

MAX_WORD_LENGTH = 20
