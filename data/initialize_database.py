import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from parse.primary import frequency_list, pronouncing_dictionary
from parse.secondary.absolute_chain import AbsoluteChain
from parse.secondary.most_probable_words import MostProbableWords
from database import connect, disconnect 
from parse.schema import schema, words, phonemes, scores

########### PHASE ZERO ####################

connection = connect()
schema(connection)

########### PHASE ONE ####################

word_frequencies = frequency_list.parse()
parsed_pronouncing_dictionary = pronouncing_dictionary.parse(word_frequencies)
words(connection, parsed_pronouncing_dictionary['words_for_db'])

########### PHASE TWO ####################

most_probable_next_phonemes = {'weighted': {}, 'unweighted': {}}
for stressless in [False, True]:
	stress_consideration = '_stressless' if stressless else ''
	stress_consideration_key = 'stressless' if stressless else 'with_stress'

	most_probable_next_phonemes['weighted'][stress_consideration_key] = AbsoluteChain.parse(
		parsed_pronouncing_dictionary['phoneme_chain_absolute{}'.format(
			stress_consideration
		)]
	)
	most_probable_next_phonemes['unweighted'][stress_consideration_key] = AbsoluteChain.parse(
		parsed_pronouncing_dictionary['phoneme_chain_absolute_unweighted{}'.format(
			stress_consideration
		)]
	)

	phonemes(
		connection,
		most_probable_next_phonemes['weighted'][stress_consideration_key],
		most_probable_next_phonemes['unweighted'][stress_consideration_key],
		stressless
	)

########### PHASE THREE ####################

for stressless in [False, True]:
	for unweighted in [False, True]:
		for method_mean in [False, True]:
			for method_addition in [False, True]:
				weighting = 'unweighted' if unweighted else 'weighted'
				stress_consideration_key = 'stressless' if stressless else 'with_stress'				
				most_probable_words = MostProbableWords.get(
					most_probable_next_phonemes[weighting][stress_consideration_key],
					stressless, 
					unweighted, 
					method_mean, 
					method_addition
				)
				scores(
					connection, 
					most_probable_words, 
					stressless, 
					unweighted, 
					method_mean, 
					method_addition
				)

disconnect(connection)