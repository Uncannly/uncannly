import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.present import Present
from lib.type_conversion import array_to_string
from lib.score import get_score
from data.load_data import load_phonemes

next_phonemes_weighted = load_phonemes(unweighted=False, unstressed=False)
next_phonemes_unweighted = load_phonemes(unweighted=True, unstressed=False)
next_phonemes_weighted_unstressed = load_phonemes(unweighted=False, unstressed=True)
next_phonemes_unweighted_unstressed = load_phonemes(unweighted=True, unstressed=True)

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

		phoneme = 'START_WORD'
		score = 1.0
		word = []

		misses = 0
		count = 0
		output = []

		if selection:
			selector = api_select_top if interface == 'api' else bin_select_top
		else:
			selector = api_select_random if interface == 'api' else bin_select_random

		while True:
			phoneme_tuple = next_phoneme(
				phoneme, 
				random.random(), 
				len(word) + 1,
				score, 
				scoring_method, 
				score_threshold, 
				unweighted,
				unstressed
			)

			if phoneme_tuple == None:
				misses += 1
				if misses > 1000000:
					message = '1000000 times consecutively failed to find a word above the score threshold. Please try lowering it.'
					if interface == "bin":
						sys.stdout.write(message + '\n')
						return
					elif interface == "api":
						return [message]
				phoneme = 'START_WORD'
				word = []
			else:
				misses = 0
				phoneme = phoneme_tuple[0]
				score = phoneme_tuple[1]
				if phoneme == 'END_WORD':
					selected_word = selector(word, unstressed, exclude_real)
					if selected_word:
						output.append((selected_word, score))
						count += 1
						if count == pool:
							if selection is not None:
								output.sort(key=lambda x: -x[1])
								if selection < pool:
									output = output[:selection]
							
							length = len(output)

							if interface == 'api':
								return [x[0] for x in output]
							else:
								for (out, put) in output:
									sys.stdout.write(out + '\n')
								if length < selection:
									sys.stdout.write(
										'Fewer words met criteria than the specified return count.\n'
									)
								return
					phoneme = 'START_WORD'
					word = []
					score = 1.0
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
	if unstressed:
		next_phonemes = next_phonemes_unweighted_unstressed if unweighted else next_phonemes_weighted_unstressed
	else:
		next_phonemes = next_phonemes_unweighted if unweighted else next_phonemes_weighted

	accumulated_probability = 0
	for (phoneme, probability) in next_phonemes[phoneme]:
		accumulated_probability += probability
		if accumulated_probability >= random_number:
			score = get_score(score, scoring_method, probability, word_length)
			return None if score < score_threshold else (phoneme, score)

def bin_select_top(word, unstressed, exclude_real):
	stringified_word = array_to_string(word)
	return Present.for_terminal(stringified_word, unstressed, exclude_real, suppress_immediate=True)

def bin_select_random(word, unstressed, exclude_real):
	stringified_word = array_to_string(word)
	return Present.for_terminal(stringified_word, unstressed, exclude_real, suppress_immediate=True)

def api_select_top(word, unstressed, exclude_real):
	return Present.for_web(word, unstressed, exclude_real)
	
def api_select_random(word, unstressed, exclude_real):
	return Present.for_web(word, unstressed, exclude_real)
		