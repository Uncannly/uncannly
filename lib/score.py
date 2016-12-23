def get_score(score, scoring_method, probability, word_length):

  if (scoring_method == 'integral_product'):
    score = score * probability

  elif (scoring_method == 'integral_sum'):
    score = 1 / ((1 / score) + (1 - probability))

  elif (scoring_method == 'mean_geometric'):
    previous_weighted_probability = score ** word_length
    multiply_in_new_probability = previous_weighted_probability * probability
    root = 1.0 / float(word_length)
    score = multiply_in_new_probability ** root

  elif (scoring_method == 'mean_arithmetic'):
    score = ((score * (word_length)) + probability) / (word_length + 1)

  return score