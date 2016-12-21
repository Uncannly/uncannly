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
				if count_fails > 1000000:
					return fail(interface)
				word, phoneme, score = reset()
			else:
				count_fails = 0
				if phoneme == 'END_WORD':
					selected_word = selector(word, unstressed, exclude_real)
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

	if unstressed:
		if unweighted:
			next_phonemes = next_phonemes_unweighted_unstressed
		else:
			next_phonemes = next_phonemes_weighted_unstressed
	else:
		if unweighted:
			next_phonemes = next_phonemes_unweighted
		else:
			next_phonemes = next_phonemes_weighted

	accumulated_probability = 0
	for (phoneme, probability) in next_phonemes[phoneme]:
		accumulated_probability += probability
		if accumulated_probability >= random_number:
			score = get_score(score, scoring_method, probability, word_length)
			return (None, score) if score < score_threshold else (phoneme, score)

def bin_selector(word, unstressed, exclude_real):
	stringified_word = array_to_string(word)
	return Present.for_terminal(stringified_word, unstressed, exclude_real, suppress_immediate=True)

def api_selector(word, unstressed, exclude_real):
	return Present.for_web(word, unstressed, exclude_real)
		
def reset():
	return ([], 'START_WORD', 1.0)

def fail(interface):
	message = '1000000 times consecutively failed to find a word \
		above the score threshold. Please try lowering it.'
	return sys.stdout.write(message + '\n') if interface == "bin" else [message]

def succeed(words, interface, selection):
	if selection:
		words.sort(key=lambda x: -x[1])
		words = words[:selection]
	
	if interface == 'bin':
		for word, _ in words:
			sys.stdout.write(word + '\n')
		if len(words) < selection:
			sys.stdout.write(
				'Fewer words met criteria than the specified return count.\n'
			)
	else:
		return [x[0] for x in words]
		