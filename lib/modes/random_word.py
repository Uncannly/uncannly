import random, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib.present import Present
from lib.secondary_data_io import load
from lib.type_conversion import array_to_string
from lib.score import get_score

next_phonemes_weighted = load('most_probable_next_phonemes')
next_phonemes_unweighted = load('most_probable_next_phonemes_unweighted')

class RandomWord:
	@staticmethod
	def get(
		interface, 
		return_count, # thrown away
		random_selection, # thrown away
		scoring_method, 
		score_threshold, 
		unweighted, 
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
				unweighted
			)

			if phoneme_tuple == None:
				misses += 1
				if misses > 1000000:
					message = '1000000 times consecutively failed to find a word above the score threshold. Please try lowering it.'
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
						word_was_presented = Present.for_terminal(stringified_word, exclude_real)
						if word_was_presented == True:
							return
						else:
							phoneme = 'START_WORD'
							word = []
					elif interface == "api":
						word_to_present = Present.for_web(word, exclude_real)
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
	unweighted):
	next_phonemes = next_phonemes_unweighted if unweighted else next_phonemes_weighted

	accumulated_probability = 0
	for (phoneme, probability) in next_phonemes[phoneme]:
		accumulated_probability += probability
		if accumulated_probability >= random_number:
			score = get_score(score, scoring_method, probability, word_length)
			return None if score < score_threshold else (phoneme, score)