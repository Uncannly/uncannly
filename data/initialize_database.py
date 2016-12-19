import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.parse.primary import frequency_list, pronouncing_dictionary
from lib.parse.secondary.absolute_chain import AbsoluteChain
from lib.parse.secondary.most_probable_words import MostProbableWords
from data.database import do_the_schema, do_the_words_table, do_a_phoneme_chain, do_some_scores

########### PHASE ZERO ####################

do_the_schema()

########### PHASE ONE ####################

word_frequencies = frequency_list.parse()
parsed_pronouncing_dictionary = pronouncing_dictionary.parse(word_frequencies)
do_the_words_table(parsed_pronouncing_dictionary['words_for_db'])

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

	do_a_phoneme_chain(
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
				do_some_scores(most_probable_words, stressless, unweighted, method_mean, method_addition)