import time, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import file, frequency_list, pronouncing_dictionary, absolute_chain, most_probable_next_phonemes

# parse frequency list
word_frequencies = frequency_list.parse()

# use frequency list as weight on absolute phoneme chain
parsed_pronouncing_dictionary = pronouncing_dictionary.parse(word_frequencies)
phoneme_chain_absolute = parsed_pronouncing_dictionary['phoneme_chain_absolute']

# also receive two analogous lists of words and their pronounciations
file.save(
	parsed_pronouncing_dictionary['words'], 
	'words'
)
file.save(
	parsed_pronouncing_dictionary['word_pronunciations'],
	'word_pronunciations'
)

# use absolute phoneme chain to create structures used directly by features
parsed_absolute_chain = absolute_chain.parse(phoneme_chain_absolute)
file.save(
	parsed_absolute_chain['cumulative_distributions'],
	'cumulative_distributions'
)
# file.save(
# 	parsed_absolute_chain['most_probable_next_phonemes'],
# 	'most_probable_next_phonemes'
# )

most_probable_words = most_probable_next_phonemes.parse(
	parsed_absolute_chain['most_probable_next_phonemes']
)
file.save(most_probable_words, 'most_probable_words')