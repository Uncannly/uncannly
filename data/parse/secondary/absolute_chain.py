class AbsoluteChain:
	@staticmethod
	def parse(phoneme_chain_absolute):
		this_phonemes_most_probable_next_phonemes = {}

		for phoneme, next_phoneme_occurrences in phoneme_chain_absolute.iteritems():
			this_phonemes_most_probable_next_phonemes[phoneme] = \
				most_probable_next_phonemes(next_phoneme_occurrences)

		return this_phonemes_most_probable_next_phonemes

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