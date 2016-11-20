def cumulative_distribution(next_phoneme_occurrences):
	total_occurrences_of_next_phonemes = sum(next_phoneme_occurrences.itervalues())
	cumulative_distribution = []
	accumulated_probability = 0.0

	for next_phoneme, occurrences in next_phoneme_occurrences.iteritems():
		probability = float(occurrences) / float(total_occurrences_of_next_phonemes)
		accumulated_probability += probability
		cumulative_distribution.append({
			'next_phoneme': next_phoneme, 
			'accumulated_probability': accumulated_probability
		})
		
	return cumulative_distribution