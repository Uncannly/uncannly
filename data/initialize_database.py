import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from parse.primary import frequency_list, pronouncing_dictionary
from parse.secondary.absolute_chain import AbsoluteChain
from parse.secondary.most_probable_words import MostProbableWords
from database import Database 
from schema import Schema

########### PHASE ZERO ####################

schema = Schema(Database())
schema.schema()

########### PHASE ONE ####################

word_frequencies = frequency_list.parse()
parsed_pronouncing_dictionary = pronouncing_dictionary.parse(word_frequencies)
schema.words(parsed_pronouncing_dictionary['words'])

########### PHASE TWO ####################

most_probable_next_phonemes = {'weighted': {}, 'unweighted': {}}
for unstressed in [False, True]:
	stress_consideration = '_unstressed' if unstressed else ''
	stress_consideration_key = 'unstressed' if unstressed else 'stressed'

	most_probable_next_phonemes['weighted'][stress_consideration_key] = AbsoluteChain.parse(
		parsed_pronouncing_dictionary['phoneme_chains']['weighted'][stress_consideration_key]
	)
	most_probable_next_phonemes['unweighted'][stress_consideration_key] = AbsoluteChain.parse(
		parsed_pronouncing_dictionary['phoneme_chains']['unweighted'][stress_consideration_key]
	)

	schema.phonemes(
		most_probable_next_phonemes['weighted'][stress_consideration_key],
		most_probable_next_phonemes['unweighted'][stress_consideration_key],
		unstressed
	)

########### PHASE THREE ####################

for unstressed in [False, True]:
	for unweighted in [False, True]:
		for method_mean in [False, True]:
			for method_addition in [False, True]:
				weighting = 'unweighted' if unweighted else 'weighted'
				stress_consideration_key = 'unstressed' if unstressed else 'stressed'				
				most_probable_words = MostProbableWords.get(
					most_probable_next_phonemes[weighting][stress_consideration_key],
					unstressed, 
					unweighted, 
					method_mean, 
					method_addition
				)
				schema.scores(
					most_probable_words, 
					unstressed, 
					unweighted, 
					method_mean, 
					method_addition
				)

schema.finish()

sys.stdout.write('Database successfully initialized.\n')