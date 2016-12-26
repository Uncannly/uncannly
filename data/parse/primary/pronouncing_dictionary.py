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
        for stressing in ['stressed', 'unstressed']:
            for weighting in ['weighted', 'unweighted']:
                self.phoneme_chains.setdefault(weighting, {}).setdefault(stressing, [{}])
                for i in range(0, len(phonemes[stressing]) - 1):
                    phoneme = phonemes[stressing][i] 
                    next_phoneme = phonemes[stressing][i + 1]

                    self.phoneme_chains[weighting][stressing][0].\
                        setdefault(phoneme, {}).setdefault(next_phoneme, 0)
                    self.phoneme_chains[weighting][stressing][0][phoneme][next_phoneme] \
                        += frequency if weighting == 'weighted' else 1

                    while i + 2 > len(self.phoneme_chains[weighting][stressing]):
                        self.phoneme_chains[weighting][stressing].append({})

                    self.phoneme_chains[weighting][stressing][i + 1].\
                        setdefault(phoneme, {}).setdefault(next_phoneme, 0)
                    self.phoneme_chains[weighting][stressing][i + 1][phoneme][next_phoneme] \
                        += frequency if weighting == 'weighted' else 1
