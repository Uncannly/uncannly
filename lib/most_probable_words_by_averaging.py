import most_probable_words

def parse(most_probable_next_phonemes):
	return most_probable_words.parse(most_probable_next_phonemes, 'averaging')
	# most_probable_words = {}

	# def next_phoneme(word, average_probability):
	# 	current_phoneme = word[len(word) - 1]

	# 	if len(word) > 20:
	# 		pass
	# 	else:
	# 		for pp_tuple in most_probable_next_phonemes[current_phoneme]:
	# 			phoneme = pp_tuple[0]
	# 			probability = pp_tuple[1]
	# 			average_probability = ((len(word) * average_probability) + probability) / (len(word) + 1)

	# 			if average_probability < 0.2415:
	# 				pass
	# 			elif phoneme == 'END_WORD':
	# 				formatted_word = format.format(word)
	# 				most_probable_words[formatted_word] = average_probability
	# 			else:	
	# 				grown_word = word[:]
	# 				grown_word.append(phoneme)
	# 				next_phoneme(grown_word, average_probability)

	# next_phoneme(['START_WORD'], 1.0)

	# return most_probable_words