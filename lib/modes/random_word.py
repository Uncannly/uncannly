import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.present import Present
from lib.type_conversion import array_to_string
from lib.score import get_score
from data.load_data import load_phonemes

next_phonemes_weighted = load_phonemes(unweighted=False, stress_ignored=False)
next_phonemes_unweighted = load_phonemes(unweighted=True, stress_ignored=False)
next_phonemes_weighted_stress_ignored = load_phonemes(unweighted=False, stress_ignored=True)
next_phonemes_unweighted_stress_ignored = load_phonemes(unweighted=True, stress_ignored=True)

class RandomWord:
	@staticmethod
	def get(
		interface, 
		return_count, # thrown away
		random_selection, # thrown away
		scoring_method, 
		score_threshold, 
		unweighted, 
		ignore_stress,
		exclude_real):

		phoneme = 'START_WORD'
		score = 1.0
		word = []
		misses = 0
		while True:
			phoneme_tuple = next_phoneme(
				phoneme, 
				random.random(), 
				len(word) + 1,
				score, 
				scoring_method, 
				score_threshold, 
				unweighted,
				ignore_stress
			)

			if phoneme_tuple == None:
				misses += 1
				if misses > 10000:
					message = '10000 times consecutively failed to find a word above the score threshold. Please try lowering it.'
					if interface == "bin":
						sys.stdout.write(message + '\n')
						return
					elif interface == "api":
						return message
				phoneme = 'START_WORD'
				word = []
			else:
				misses = 0
				phoneme = phoneme_tuple[0]
				score = phoneme_tuple[1]
				if phoneme == 'END_WORD':
					if interface == "bin":
						stringified_word = array_to_string(word)
						word_was_presented = Present.for_terminal(stringified_word, ignore_stress, exclude_real)
						if word_was_presented == True:
							return
						else:
							phoneme = 'START_WORD'
							word = []
					elif interface == "api":
						word_to_present = Present.for_web(word, ignore_stress, exclude_real)
						if word_to_present != None:
							return word_to_present
						else:
							phoneme = 'START_WORD'
							word = []
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
	ignore_stress):
	if ignore_stress:
		next_phonemes = next_phonemes_unweighted_stress_ignored if unweighted else next_phonemes_weighted_stress_ignored
	else:
		next_phonemes = next_phonemes_unweighted if unweighted else next_phonemes_weighted

	accumulated_probability = 0
	for (phoneme, probability) in next_phonemes[phoneme]:
		accumulated_probability += probability
		if accumulated_probability >= random_number:
			score = get_score(score, scoring_method, probability, word_length)
			return None if score < score_threshold else (phoneme, score)