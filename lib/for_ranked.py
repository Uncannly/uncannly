def ranked_most_likely_next_phonemes_for_this_phoneme(potential_next_phonemes, simple_probability_of_each_potential_next_phoneme):
	chances = []
	for potential_next_phoneme, chance in simple_probability_of_each_potential_next_phoneme.iteritems():
		chances.append(chance)
	chances.sort(reverse=True)

	ranked_most_likely_next_phonemes = []
	for chance in chances:
		ranked_most_likely_next_phonemes.append(simple_probability_of_each_potential_next_phoneme.keys()[simple_probability_of_each_potential_next_phoneme.values().index(chance)])
	return ranked_most_likely_next_phonemes