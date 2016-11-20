def most_probable_next_phonemes(next_phoneme_occurrences):
	return sorted(
		next_phoneme_occurrences, 
		key = next_phoneme_occurrences.get, 
		reverse = True
	)