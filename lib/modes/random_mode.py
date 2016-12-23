import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.present import Present
from lib.type_conversion import array_to_string
from lib.score import get_score
from lib.options import booleans_to_strings
from data.load_data import load_phonemes

next_phonemes_options = {}
for unstressed in [False, True]:
	for unweighted in [False, True]:
		stressing, weighting = booleans_to_strings(unstressed, unweighted)
		next_phonemes_options.setdefault(stressing, {}).setdefault(
			weighting, load_phonemes(unweighted, unstressed)
		)

class RandomMode:
	@staticmethod
	def get(
		interface, 
		pool,
		selection,
		scoring_method, 
		score_threshold, 
		unweighted, 
		unstressed,
		exclude_real):

		selector = api_selector if interface == 'api' else bin_selector

		word, phoneme, score = reset()

		count_fails = 0
		count_successes = 0
		words = []

		while True:
			phoneme, score = next_phoneme(
				phoneme=phoneme, 
				random_number=random.random(), 
				word_length=len(word) + 1,
				score=score, 
				scoring_method=scoring_method, 
				score_threshold=score_threshold, 
				unweighted=unweighted,
				unstressed=unstressed
			)

			if phoneme == None:
				count_fails += 1
				if count_fails > 10000:
					return fail(interface)
				word, phoneme, score = reset()
			else:
				count_fails = 0
				if phoneme == 'END_WORD':
					selected_word = selector(word, selection, unstressed, exclude_real)
					if selected_word:
						words.append((selected_word, score))
						count_successes += 1
						if count_successes == pool:
							return succeed(words, interface, selection)
					word, phoneme, score = reset()
				else:
					word.append(phoneme)

def next_phoneme(
	phoneme, 
	random_number, 
	word_length,
	score, 
	scoring_method, 
	score_threshold, 
	unweighted,
	unstressed):

	stressing, weighting = booleans_to_strings(unstressed, unweighted)
	next_phonemes = next_phonemes_options[stressing][weighting]

	accumulated_probability = 0
	for (phoneme, probability) in next_phonemes[phoneme]:
		accumulated_probability += probability
		if accumulated_probability >= random_number:
			score = get_score(score, scoring_method, probability, word_length)
			return (None, score) if score < score_threshold else (phoneme, score)

def bin_selector(word, selection, unstressed, exclude_real):
	stringified_word = array_to_string(word)
	return Present.for_terminal(
		word=stringified_word, 
		unstressed=unstressed, 
		exclude_real=exclude_real, 
		suppress_immediate=selection
	)

def api_selector(word, selection, unstressed, exclude_real):
	return Present.for_web(word, unstressed, exclude_real)
		
def reset():
	return ([], 'START_WORD', 1.0)

def fail(interface):
	message = (
		'10000 times consecutively failed to find a word above the score threshold.' 
		'Please try lowering it.'
	)
	return sys.stdout.write(message + '\n') if interface == "bin" else [message]

def succeed(words, interface, selection):
	if selection:
		words.sort(key=lambda x: -x[1])
		words = words[:selection]
	
	if interface == 'bin':
		if selection:
			for word, _ in words:
				sys.stdout.write(word + '\n')
	else:
		return [x[0] for x in words]
