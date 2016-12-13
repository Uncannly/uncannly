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


########### PHASE THREE ####################

 
# create a set of one million or so most probable words
most_probable_words = {}

# strategy A1 uses an integral, product
most_probable_words['by_integral_product'] = \
	MostProbableWords.get(
		most_probable_next_phonemes, 'weighted', 'integral_product'
	)
save(
	most_probable_words['by_integral_product'], 
	'most_probable_words_by_integral_product_weighted'
)

# strategy A2 uses an integral, sum
most_probable_words['by_integral_sum'] = \
	MostProbableWords.get(
		most_probable_next_phonemes, 'weighted', 'integral_sum'
	)
save(
	most_probable_words['by_integral_sum'], 
	'most_probable_words_by_integral_sum_weighted'
)

# strategy B1 uses a mean, geometric
most_probable_words['by_mean_geometric'] = \
	MostProbableWords.get(
		most_probable_next_phonemes, 'weighted', 'mean_geometric'
	)
save(
	most_probable_words['by_mean_geometric'], 
	'most_probable_words_by_mean_geometric_weighted'
)

# strategy B2 uses a mean, arithmetic
most_probable_words['by_mean_arithmetic'] = \
	MostProbableWords.get(
		most_probable_next_phonemes, 'weighted', 'mean_arithmetic'
	)
save(
	most_probable_words['by_mean_arithmetic'], 
	'most_probable_words_by_mean_arithmetic_weighted'
)

# repeat all above strategies for unweighted versions
most_probable_words['by_integral_product_unweighted'] = \
	MostProbableWords.get(
		most_probable_next_phonemes_unweighted, 'unweighted', 'integral_product'
	)
save(
	most_probable_words['by_integral_product_unweighted'], 
	'most_probable_words_by_integral_product_unweighted'
)
most_probable_words['by_integral_sum_unweighted'] = \
	MostProbableWords.get(
		most_probable_next_phonemes_unweighted, 'unweighted', 'integral_sum'
	)
save(
	most_probable_words['by_integral_sum_unweighted'], 
	'most_probable_words_by_integral_sum_unweighted'
)
most_probable_words['by_mean_geometric_unweighted'] = \
	MostProbableWords.get(
		most_probable_next_phonemes_unweighted, 'unweighted', 'mean_geometric'
	)
save(
	most_probable_words['by_mean_geometric_unweighted'], 
	'most_probable_words_by_mean_geometric_unweighted'
)
most_probable_words['by_mean_arithmetic_unweighted'] = \
	MostProbableWords.get(
		most_probable_next_phonemes_unweighted, 'unweighted', 'mean_arithmetic'
	)
save(
	most_probable_words['by_mean_arithmetic_unweighted'], 
	'most_probable_words_by_mean_arithmetic_unweighted'
)