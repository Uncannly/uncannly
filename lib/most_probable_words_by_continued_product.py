import most_probable_words

def parse(most_probable_next_phonemes):
	return most_probable_words.parse(most_probable_next_phonemes, 'continued_product')

# import format

# def parse(most_probable_next_phonemes):
# 	most_probable_words = {}

# 	def next_phoneme(word, probability_continued_product):
# 		current_phoneme = word[len(word) - 1]

# 		for pp_tuple in most_probable_next_phonemes[current_phoneme]:
# 			phoneme = pp_tuple[0]
# 			probability = pp_tuple[1]
# 			probability_continued_product *= probability

# 			if probability_continued_product < 0.0000000000000000000001:
# 				pass
# 			elif phoneme == 'END_WORD':
# 				formatted_word = format.format(word)
# 				most_probable_words[formatted_word] = probability_continued_product
# 			else:	
# 				grown_word = word[:]
# 				grown_word.append(phoneme)
# 				next_phoneme(grown_word, probability_continued_product)

# 	next_phoneme(['START_WORD'], 1.0)

# 	return most_probable_words