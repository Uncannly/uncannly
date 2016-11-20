import file

phoneme_chain_absolute = {}

def pronouncing_dictionary(word_freqs):
	words = []
	phonetic_words = []

	f = open('primary_data/cmu_pronouncing_dictionary.txt', 'r')
	for line in f:
		split_by_tabs = line.strip().split('\t')
		word = split_by_tabs[0]

		freq = float(word_freqs[word]) if word in word_freqs else 1.0

		words.append(word)
		phonetic_word = split_by_tabs[1]
		store_phonemes_for_word(freq, phonetic_word, phonetic_words)
	f.close()

	file.save(phonetic_words, 'phonetic_words')
	file.save(words, 'words')

	return phoneme_chain_absolute

# private

def store_phoneme_transition_instance(freq, first_phoneme, second_phoneme):
	phoneme_chain_absolute.setdefault(first_phoneme, {}).setdefault(second_phoneme, 0)
	phoneme_chain_absolute[first_phoneme][second_phoneme] += freq

def store_phonemes_for_word(freq, phonetic_word, phonetic_words):
	phonemes = phonetic_word.split()
	for i in range(0, len(phonemes)):
		phonemes[i] = phonemes[i].strip('012')
	phonetic_words.append(" ".join(phonemes))
	phonemes.insert(0, 'START_WORD')
	phonemes.append('END_WORD')
	for i in range(0, len(phonemes) - 1):
		store_phoneme_transition_instance(freq, phonemes[i], phonemes[i + 1])
