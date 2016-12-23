def booleans_to_strings(unstressed, unweighted):
  stressing = 'unstressed' if unstressed else 'stressed'
  weighting = 'unweighted' if unweighted else 'weighted'
  return stressing, weighting

scoring_methods = {
    'integral_product': (False, False),
    'integral_sum': (False, True),
    'mean_geometric': (True, False),
    'mean_arithmetic': (True, True),
}

# these are all ~10000, which is more than the 1000 of each
# which we are actually capable of fitting in our free plan cloud database
default_limits = {
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

pool_default = 45
pool_max = 1000