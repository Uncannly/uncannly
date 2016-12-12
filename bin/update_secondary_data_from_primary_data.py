import time, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.secondary_data_io import save
from lib.parse.primary import frequency_list, pronouncing_dictionary
from lib.parse.secondary.absolute_chain import AbsoluteChain
from lib.parse.secondary.most_probable_words import MostProbableWords


########### PHASE ONE ####################


# parse frequency list
word_frequencies = frequency_list.parse()

# use frequency list to make weighting an option
parsed_pronouncing_dictionary = pronouncing_dictionary.parse(word_frequencies)

# receive two analogous lists: all words, and their pronounciations
save(parsed_pronouncing_dictionary['words'], 'words')
save(parsed_pronouncing_dictionary['word_pronunciations'], 'word_pronunciations')


########### PHASE TWO ####################


# from absolute phoneme chain, create sorted data structure for everything else
phoneme_chain_absolute = \
	parsed_pronouncing_dictionary['phoneme_chain_absolute']
most_probable_next_phonemes = \
	AbsoluteChain.parse(phoneme_chain_absolute)
save(
	most_probable_next_phonemes, 
	'most_probable_next_phonemes'
)

# also do this for the unweighted version
phoneme_chain_absolute_unweighted = \
	parsed_pronouncing_dictionary['phoneme_chain_absolute_unweighted']
most_probable_next_phonemes_unweighted = \
	AbsoluteChain.parse(phoneme_chain_absolute_unweighted)
save(
	most_probable_next_phonemes_unweighted, 
	'most_probable_next_phonemes_unweighted'
)


########### PHASE THREE.ONE ####################

 
# create a set of one million or so most probable words
most_probable_words = {}

# strategy one uses an integral product
most_probable_words['by_integral_product'] = \
	MostProbableWords.by_integral_product(most_probable_next_phonemes)
save(
	most_probable_words['by_integral_product'], 
	'most_probable_words_by_integral_product_weighted'
)

# strategy two uses a mean, arithmetic
most_probable_words['by_mean_arithmetic'] = \
	MostProbableWords.by_mean_arithmetic(most_probable_next_phonemes)
save(
	most_probable_words['by_mean_arithmetic'], 
	'most_probable_words_by_mean_arithmetic_weighted'
)


# repeat both above strategies for unweighted versions
most_probable_words['by_integral_product_unweighted'] = \
	MostProbableWords.by_integral_product(most_probable_next_phonemes_unweighted)
save(
	most_probable_words['by_integral_product_unweighted'], 
	'most_probable_words_by_integral_product_unweighted'
)
most_probable_words['by_mean_arithmetic_unweighted'] = \
	MostProbableWords.by_mean_arithmetic(most_probable_next_phonemes_unweighted)
save(
	most_probable_words['by_mean_arithmetic_unweighted'], 
	'most_probable_words_by_mean_arithmetic_unweighted'
)