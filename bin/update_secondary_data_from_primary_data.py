import time, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import file, frequency_list, pronouncing_dictionary, absolute_chain

word_frequencies = frequency_list.parse()
parsed_pronouncing_dictionary = pronouncing_dictionary.parse(word_frequencies)

phoneme_chain_absolute = parsed_pronouncing_dictionary['phoneme_chain_absolute']
phonetic_words = parsed_pronouncing_dictionary['phonetic_words']
words = parsed_pronouncing_dictionary['words']

parsed_absolute_chain = absolute_chain.parse(phoneme_chain_absolute)

cumulative_distributions = parsed_absolute_chain['cumulative_distributions']
most_probable_next_phonemes = parsed_absolute_chain['most_probable_next_phonemes']

file.save(cumulative_distributions, 'cumulative_distributions')
file.save(most_probable_next_phonemes, 'most_probable_next_phonemes')
file.save(phonetic_words, 'phonetic_words')
file.save(words, 'words')