import cumulative_distribution, most_probable_next_phonemes

def parse(phoneme_chain_absolute):
	cumulative_distributions = {}
	this_phonemes_most_probable_next_phonemes = {}

	for phoneme, next_phoneme_occurrences in phoneme_chain_absolute.iteritems():
		cumulative_distributions[phoneme] = \
			cumulative_distribution.get(next_phoneme_occurrences)
		this_phonemes_most_probable_next_phonemes[phoneme] = \
			most_probable_next_phonemes.get(next_phoneme_occurrences)

	return {
		'cumulative_distributions': cumulative_distributions,
		'most_probable_next_phonemes': this_phonemes_most_probable_next_phonemes
	}