import time, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import file, parse, for_ranked, for_random

word_freqs = parse.frequency_list()
phoneme_chain_absolute = parse.pronouncing_dictionary(word_freqs)

cumulative_distributions = {}
simple_probabilities_of_potential_next_phonemes_per_phoneme = {}
ranked_most_likely_next_phonemes_per_phoneme = {}

for phoneme, potential_next_phonemes in phoneme_chain_absolute.iteritems():
	cumulative_distributions[phoneme] = for_random.cumulative_distribution(potential_next_phonemes)
	simple_probabilities_of_potential_next_phonemes_per_phoneme[phoneme] = for_random.simple_probabilities_of_potential_next_phonemes(potential_next_phonemes)
	ranked_most_likely_next_phonemes_per_phoneme[phoneme] = for_ranked.ranked_most_likely_next_phonemes_for_this_phoneme(potential_next_phonemes, simple_probabilities_of_potential_next_phonemes_per_phoneme[phoneme])

file.save(cumulative_distributions, 'cumulative_distributions')
file.save(ranked_most_likely_next_phonemes_per_phoneme, 'ranked_most_likely_next_phonemes_per_phoneme')