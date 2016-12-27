from data.parse.primary.open_helper import open_primary_data_file
from lib.ipa import destress

class PronouncingDictionary(object):
    def __init__(self, word_frequencies):
        self.words = []
        self.phoneme_chains = {}
        self.pronouncing_dictionary = open_primary_data_file('cmu_pronouncing_dictionary')
        self.word_frequencies = word_frequencies

    def parse(self):
        for line in self.pronouncing_dictionary:
            self.parse_phoneme_chains(self.parse_words(line))

        self.pronouncing_dictionary.close()

        return self.words, self.phoneme_chains

    def parse_words(self, line):
        [word, word_pronunciation] = line.strip().split('\t')

        phonemes = {}
        phonemes['stressed'] = word_pronunciation.split()
        phonemes['unstressed'] = [destress(phoneme) for phoneme in phonemes['stressed']]

        self.words.append((word, word_pronunciation))

        for stressing in ['stressed', 'unstressed']:
            phonemes[stressing] = ['START_WORD'] + phonemes[stressing] + ['END_WORD']

        frequency = self.word_frequencies[word] if word in self.word_frequencies else 1

        return phonemes, frequency

    def parse_phoneme_chains(self, args):
        phonemes, frequency = args
        for weighting in ['weighted', 'unweighted']:
            for stressing in ['stressed', 'unstressed']:
                self.phoneme_chains.setdefault(weighting, {}).setdefault(stressing, [])
                word_length = len(phonemes[stressing])

                for word_position in range(0, word_length - 1):
                    phoneme = phonemes[stressing][word_position] 
                    next_phoneme = phonemes[stressing][word_position + 1]

                    for ignore_length in [False, True]:
                        length = 0 if ignore_length else word_length - 2 # for start_word and end_word
                        while length + 1 > len(self.phoneme_chains[weighting][stressing]):
                            self.phoneme_chains[weighting][stressing].append([])

                        for ignore_position in [False, True]:
                            position = 0 if ignore_position else word_position + 1 # bc word_position is also 0-indexed but we need it to start in index 1 since 0 is reserved for the catch-all (btw, the index 1 has only one key, START_WORD)
                            while position + 1 > len(self.phoneme_chains[weighting][stressing][length]):
                                self.phoneme_chains[weighting][stressing][length].append({})

                            self.phoneme_chains[weighting][stressing][length][position].\
                                setdefault(phoneme, {}).setdefault(next_phoneme, 0)
                            self.phoneme_chains[weighting][stressing][length][position]\
                                [phoneme][next_phoneme] += frequency if weighting == 'weighted' else 1