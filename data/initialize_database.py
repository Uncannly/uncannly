import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.parse.primary import frequency_list, pronouncing_dictionary
from lib.parse.secondary.absolute_chain import AbsoluteChain
from lib.parse.secondary.most_probable_words import MostProbableWords
from data.database import connect, disconnect, do_the_words_table, do_a_phoneme_chain

########### PHASE ZERO ####################

connection = connect()
cur = connection.cursor()
sql = ";".join([
	"drop table if exists words",
	"create table words (word varchar, \
		pronunciation varchar, pronunciation_stressless varchar)",
	"drop table if exists phonemes",
	"create table phonemes (phoneme varchar, stressless boolean, \
		next_phonemes varchar, next_phonemes_unweighted varchar)",
	"drop table if exists scores",
	"create table scores (word varchar, score float(25), \
		stressless boolean, unweighted boolean, \
		method_mean boolean, method_addition boolean)",
	""
])
cur.execute(sql)
cur.close()
disconnect(connection)

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
				MostProbableWords.get(
					most_probable_next_phonemes[weighting][stress_consideration_key],
					stressless, 
					unweighted, 
					method_mean, 
					method_addition
				)