def get(next_phoneme_occurrences):
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