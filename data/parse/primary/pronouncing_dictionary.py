from data.parse.primary.open_helper import open_primary_data_file
from lib.ipa import destress
from lib.options import OPTION_VALUES

class PronouncingDictionary(object):
    def __init__(self, word_frequencies):
        self.words = []
        self.phoneme_chains = {}
        self.pronouncing_dictionary = open_primary_data_file('cmu_pronouncing_dictionary')
        self.word_frequencies = word_frequencies
        self.word_lengths = {'weighted': [0], 'unweighted': [0]}

    def parse(self):
        for line in self.pronouncing_dictionary:
            self.parse_phoneme_chains(self.parse_words(line))
        self.pronouncing_dictionary.close()

        self.normalize_word_lengths()

        return self.words, self.phoneme_chains, self.word_lengths

    def parse_words(self, line):
        [word, word_pronunciation] = line.strip().split('\t')

        phonemes = {}
        phonemes['stressed'] = word_pronunciation.split()
        phonemes['unstressed'] = [destress(phoneme) for phoneme in phonemes['stressed']]

        word_length = len(phonemes['stressed'])

        for stressing in ['stressed', 'unstressed']:
            phonemes[stressing] = ['START_WORD'] + phonemes[stressing] + ['END_WORD']

        frequency = self.word_frequencies[word] if word in self.word_frequencies else 1

        self.words.append((word, word_pronunciation, frequency))

        self.length_distributions(word_length, frequency)

        return phonemes, frequency

    def parse_phoneme_chains(self, args):
        phonemes, frequency = args
        for weighting in OPTION_VALUES['weighting']:
            increment = 1 if weighting == 'unweighted' else frequency

            for stressing in OPTION_VALUES['stressing']:
                self.phoneme_chains.setdefault(weighting, {}).setdefault(stressing, [])
                word_length = len(phonemes[stressing])

                for word_position in range(0, word_length - 1):
                    phoneme = phonemes[stressing][word_position]
                    next_phoneme = phonemes[stressing][word_position + 1]

                    for ignore_length in [False, True]:
                        # the minus two is for start_word and end_word
                        length = 0 if ignore_length else word_length - 2
                        while length + 1 > len(self.phoneme_chains[weighting][stressing]):
                            self.phoneme_chains[weighting][stressing].append([])

                        for ignore_position in [False, True]:
                            # the plus 1 is because word_position is also 0-indexed
                            # but we need it to start in index 1 since 0 is reserved
                            # for the catch-all (btw, the index 1 has only one key, START_WORD)
                            position = 0 if ignore_position else word_position + 1
                            while position + 1 > len(self.phoneme_chains\
                                [weighting][stressing][length]):
                                self.phoneme_chains[weighting][stressing][length].append({})

                            self.phoneme_chains[weighting][stressing][length][position].\
                                setdefault(phoneme, {}).setdefault(next_phoneme, 0)
                            self.phoneme_chains[weighting][stressing][length][position]\
                                [phoneme][next_phoneme] += increment

    def length_distributions(self, word_length, frequency):
        for weighting in OPTION_VALUES['weighting']:
            increment = 1 if weighting == 'unweighted' else frequency

            while word_length + 1 > len(self.word_lengths[weighting]):
                self.word_lengths[weighting].append(0)

            self.word_lengths[weighting][0] += increment
            self.word_lengths[weighting][word_length] += increment

    def normalize_word_lengths(self):
        for weighting in OPTION_VALUES['weighting']:
            absolute_total_weight = self.word_lengths[weighting][0]
            for word_length in range(0, len(self.word_lengths[weighting])):
                self.word_lengths[weighting][word_length] /= float(absolute_total_weight)
