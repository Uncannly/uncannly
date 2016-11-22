def parse(phoneme_chain_absolute):
	cumulative_distributions = {}
	this_phonemes_most_probable_next_phonemes = {}

	for phoneme, next_phoneme_occurrences in phoneme_chain_absolute.iteritems():
		cumulative_distributions[phoneme] = \
			cumulative_distribution(next_phoneme_occurrences)
		this_phonemes_most_probable_next_phonemes[phoneme] = \
			most_probable_next_phonemes(next_phoneme_occurrences)

	return {
		'cumulative_distributions': cumulative_distributions,
		'most_probable_next_phonemes': this_phonemes_most_probable_next_phonemes
	}

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

def most_probable_next_phonemes(next_phoneme_occurrences):
	sorted_keys = sorted(
		next_phoneme_occurrences, 
		key = next_phoneme_occurrences.get, 
		reverse = True
	)

	total_occurrences_of_next_phonemes = sum(next_phoneme_occurrences.itervalues())
	most_probable_next_phonemes = []
	for key in sorted_keys:
		most_probable_next_phonemes.append((
			key, 
			float(next_phoneme_occurrences[key]) / float(total_occurrences_of_next_phonemes)
		))
	return most_probable_next_phonemes