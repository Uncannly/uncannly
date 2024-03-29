from sys import stdout

from lib.options import POOL_MAX

def get_score(score, scoring_method, probability, word_length):
    if scoring_method == 'integral_product':
        score = score * probability

    elif scoring_method == 'integral_sum':
        score = 1 / ((1 / score) + (1 - probability))

    elif scoring_method == 'mean_geometric':
        previous_weighted_probability = score ** word_length
        multiply_in_new_probability = previous_weighted_probability * probability
        root = 1.0 / float(word_length)
        score = multiply_in_new_probability ** root

    elif scoring_method == 'mean_arithmetic':
        score = ((score * (word_length)) + probability) / (word_length + 1)

    return score

def update_limits(count, limit, lower_limit, upper_limit):
    good_count = False
    old_limit = limit
    if count < POOL_MAX:
        upper_limit = limit
        if lower_limit:
            limit -= (limit - lower_limit) / 2
        else:
            limit /= 2
    elif count > POOL_MAX * 10:
        lower_limit = limit
        if upper_limit:
            limit += (upper_limit - limit) / 2
        else:
            limit *= 2
    else:
        good_count = True

    if limit == 0:
        stdout.write(
            'With these parameters, it is not possible '
            'to find enough words to meet the pool max.\n'
        )
        good_count = True
    elif limit != old_limit:
        stdout.write(
            'The limit for this option set has needed to change. '
            'Is this expected? If not, reconsider your commit...\n'
        )

    return good_count, limit, lower_limit, upper_limit
