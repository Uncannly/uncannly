def cumulative_distribution(potential_next_phonemes):
	total_occurrences_of_next_phonemes = sum(potential_next_phonemes.itervalues())
	cumulative_distribution = {}
	accumulated_probability = 0.0
	for potential_next_phoneme, occurrences_of_this_phoneme in potential_next_phonemes.iteritems():
		probability = occurrences_of_this_phoneme / total_occurrences_of_next_phonemes
		accumulated_probability += probability
		cumulative_distribution[potential_next_phoneme] = accumulated_probability
	return cumulative_distribution

def simple_probabilities_of_potential_next_phonemes(potential_next_phonemes):
	total_occurrences_of_next_phonemes = sum(potential_next_phonemes.itervalues())
	simple_probability_of_each_potential_next_phoneme = {}
	for potential_next_phoneme, occurrences_of_this_phoneme in potential_next_phonemes.iteritems():
		probability = occurrences_of_this_phoneme / total_occurrences_of_next_phonemes
		simple_probability_of_each_potential_next_phoneme[potential_next_phoneme] = probability
	return simple_probability_of_each_potential_next_phoneme