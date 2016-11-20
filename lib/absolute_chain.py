import for_ranked, for_random

def parse(phoneme_chain_absolute):
	cumulative_distributions = {}
	most_probable_next_phonemes = {}

	for phoneme, next_phoneme_occurrences in phoneme_chain_absolute.iteritems():
		cumulative_distributions[phoneme] = for_random.cumulative_distribution(next_phoneme_occurrences)
		most_probable_next_phonemes[phoneme] = for_ranked.most_probable_next_phonemes(next_phoneme_occurrences)

	return {
		'cumulative_distributions': cumulative_distributions,
		'most_probable_next_phonemes': most_probable_next_phonemes
	}