import time, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import file, parse

word_freqs = parse.frequency_list()
phoneme_chain_absolute = parse.pronouncing_dictionary(word_freqs)

phoneme_probabilities = {}
ranked_most_likely_next_phonemes_per_phoneme = {}

def phoneme_probabilities_for_this_phoneme(potential_next_phonemes):
	stacked_phoneme_probabability_thresholds = {}
	bleg = {}
	upper_threshold_for_this_phoneme_in_range = 0.0

	for potential_next_phoneme, num in potential_next_phonemes.iteritems():
		chance_of_this_phoneme = num / total_occurrences_of_next_phonemes
		bleg[chance_of_this_phoneme] = potential_next_phoneme
		upper_threshold_for_this_phoneme_in_range += chance_of_this_phoneme
		stacked_phoneme_probabability_thresholds[potential_next_phoneme] = upper_threshold_for_this_phoneme_in_range
	phoneme_probabilities[phoneme] = stacked_phoneme_probabability_thresholds

	return bleg

def ranked_most_likely_next_phonemes_for_this_phoneme(potential_next_phonemes, bleg):
	chances = []
	for chance, potential_next_phoneme in bleg.iteritems():
			chances.append(chance)
	chances.sort(reverse=True)

	ranked_most_likely_next_phonemes = []
	for chance in chances:
			ranked_most_likely_next_phonemes.append(bleg[chance])
	ranked_most_likely_next_phonemes_per_phoneme[phoneme] = ranked_most_likely_next_phonemes


for phoneme, potential_next_phonemes in phoneme_chain_absolute.iteritems():
	total_occurrences_of_next_phonemes = sum(potential_next_phonemes.itervalues())
	bleg = phoneme_probabilities_for_this_phoneme(potential_next_phonemes)
	ranked_most_likely_next_phonemes_for_this_phoneme(potential_next_phonemes, bleg)

file.save(phoneme_probabilities, 'phoneme_probabilities')
file.save(ranked_most_likely_next_phonemes_per_phoneme, 'ranked_most_likely_next_phonemes_per_phoneme')