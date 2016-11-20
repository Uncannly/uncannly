def most_probable_next_phonemes(next_phoneme_occurrences):
	occurrences_counts = []
	for next_phoneme, occurrences in next_phoneme_occurrences.iteritems():
		# could still override...
		occurrences_counts.append(occurrences)
	occurrences_counts.sort(reverse=True)

	most_probable_next_phonemes = []
	for occurrences_count in occurrences_counts:
		next_phonemes = next_phoneme_occurrences.keys()
		occurrences = next_phoneme_occurrences.values()
		phoneme = next_phonemes[occurrences.index(occurrences_count)]
		most_probable_next_phonemes.append(phoneme)
	return most_probable_next_phonemes