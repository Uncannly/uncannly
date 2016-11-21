def parse(word_frequencies):
	words = []
	word_pronunciations = []
	phoneme_chain_absolute = {}
	phoneme_chain_absolute_unweighted = {}

	file = open('data/primary_data/cmu_pronouncing_dictionary.txt', 'r')
	for line in file:
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

		# phoneme_chain_absolute, phoneme_chain_absolute_unweighted
		phonemes.insert(0, 'START_WORD')
		phonemes.append('END_WORD')
		frequency = word_frequencies[word] if word in word_frequencies else 1
		for i in range(0, len(phonemes) - 1):
			phoneme = phonemes[i]
			next_phoneme = phonemes[i + 1]

			phoneme_chain_absolute.setdefault(phoneme, {}).setdefault(next_phoneme, 0)
			phoneme_chain_absolute[phoneme][next_phoneme] += frequency
			
			phoneme_chain_absolute_unweighted.setdefault(phoneme, {}).setdefault(next_phoneme, 0)
			phoneme_chain_absolute_unweighted[phoneme][next_phoneme] += 1

	file.close()

	return {
		'words': words,
		'word_pronunciations': word_pronunciations,
		'phoneme_chain_absolute': phoneme_chain_absolute,
		'phoneme_chain_absolute_unweighted': phoneme_chain_absolute_unweighted
	}