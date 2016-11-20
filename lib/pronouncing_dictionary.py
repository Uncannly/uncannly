import file

def parse(word_frequencies):
	words = []
	word_pronunciations = []
	phoneme_chain_absolute = {}

	f = open('primary_data/cmu_pronouncing_dictionary.txt', 'r')
	for line in f:
		line_split_by_tabs = line.strip().split('\t')

		# words
		word = line_split_by_tabs[0]
		words.append(word)

		# word_pronunciations
		word_pronunciation = line_split_by_tabs[1]
		phonemes = word_pronunciation.split()
		for i in range(0, len(phonemes)):
			phonemes[i] = phonemes[i].strip('012')
		word_pronunciations.append(" ".join(phonemes))

		# phoneme_chain_absolute
		phonemes.insert(0, 'START_WORD')
		phonemes.append('END_WORD')
		frequency = word_frequencies[word] if word in word_frequencies else 1
		for i in range(0, len(phonemes) - 1):
			first_phoneme = phonemes[i]
			second_phoneme = phonemes[i + 1]
			phoneme_chain_absolute.setdefault(first_phoneme, {}).setdefault(second_phoneme, 0)
			phoneme_chain_absolute[first_phoneme][second_phoneme] += frequency

	f.close()

	return {
		'words': words,
		'word_pronunciations': word_pronunciations,
		'phoneme_chain_absolute': phoneme_chain_absolute
	}