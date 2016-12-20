import os

def parse(word_frequencies):
	words_for_db = []

	phoneme_chain_absolute = {}
	phoneme_chain_absolute_unweighted = {}
	phoneme_chain_absolute_unstressed = {}
	phoneme_chain_absolute_unweighted_unstressed = {}

	pwd = os.path.dirname(__file__)
	file = open(os.path.join(pwd, '..', '..', '..', 'data', 'primary_data', 'cmu_pronouncing_dictionary.txt'), 'r')

	for line in file:
		line_split_by_tabs = line.strip().split('\t')

		# words
		word = line_split_by_tabs[0]

		# word_pronunciations
		word_pronunciation = line_split_by_tabs[1]

		# word_pronunciations_unstressed
		phonemes = word_pronunciation.split()
		phonemes_unstressed = []
		for phoneme in phonemes:
			phoneme_unstressed = phoneme.strip('012')
			phonemes_unstressed.append(phoneme_unstressed)
		word_pronunciation_unstressed = " ".join(phonemes_unstressed)

		words_for_db.append((word, word_pronunciation, word_pronunciation_unstressed))

		# phoneme_chain_absolute, phoneme_chain_absolute_unweighted
		phonemes.insert(0, 'START_WORD')
		phonemes.append('END_WORD')
		phonemes_unstressed.insert(0, 'START_WORD')
		phonemes_unstressed.append('END_WORD')

		frequency = word_frequencies[word] if word in word_frequencies else 1

		for i in range(0, len(phonemes) - 1):
			phoneme = phonemes[i]
			next_phoneme = phonemes[i + 1]
			phoneme_chain_absolute.setdefault(phoneme, {}).setdefault(next_phoneme, 0)
			phoneme_chain_absolute[phoneme][next_phoneme] += frequency
			phoneme_chain_absolute_unweighted.setdefault(phoneme, {}).setdefault(next_phoneme, 0)
			phoneme_chain_absolute_unweighted[phoneme][next_phoneme] += 1

			phoneme_unstressed = phonemes_unstressed[i]
			next_phoneme_unstressed = phonemes_unstressed[i + 1]
			phoneme_chain_absolute_unstressed.setdefault(phoneme_unstressed, {}).setdefault(next_phoneme_unstressed, 0)
			phoneme_chain_absolute_unstressed[phoneme_unstressed][next_phoneme_unstressed] += frequency
			phoneme_chain_absolute_unweighted_unstressed.setdefault(phoneme_unstressed, {}).setdefault(next_phoneme_unstressed, 0)
			phoneme_chain_absolute_unweighted_unstressed[phoneme_unstressed][next_phoneme_unstressed] += 1

	file.close()

	return {
		'words_for_db': words_for_db,
		'phoneme_chain_absolute': phoneme_chain_absolute,
		'phoneme_chain_absolute_unweighted': phoneme_chain_absolute_unweighted,
		'phoneme_chain_absolute_unstressed': phoneme_chain_absolute_unstressed,
		'phoneme_chain_absolute_unweighted_unstressed': phoneme_chain_absolute_unweighted_unstressed
	}