import time, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import file, parse, for_ranked, for_random, frequency_list

word_frequencies = frequency_list.parse()
phoneme_chain_absolute = parse.pronouncing_dictionary(word_frequencies)

cumulative_distributions = {}
most_probable_next_phonemes = {}

for phoneme, next_phoneme_occurrences in phoneme_chain_absolute.iteritems():
	cumulative_distributions[phoneme] = for_random.cumulative_distribution(next_phoneme_occurrences)
	most_probable_next_phonemes[phoneme] = for_ranked.most_probable_next_phonemes(next_phoneme_occurrences)

file.save(cumulative_distributions, 'cumulative_distributions')
file.save(most_probable_next_phonemes, 'most_probable_next_phonemes')