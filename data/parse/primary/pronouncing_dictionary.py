from sys import stdout

from data.parse.primary.open_helper import open_primary_data_file
from lib.ipa import destress, parse_syllables, stress_level
from lib.options import OPTION_VALUES
from lib.conversion import sparse

# pylint: disable=too-few-public-methods
class PronouncingDictionary(object):
    def __init__(self, word_frequencies):
        self.word_frequencies = word_frequencies
        self.pronouncing_dictionary = open_primary_data_file('cmu_pronouncing_dictionary')

        self.words = []

        self.syllable_chains = {}
        self.stress_pattern_distributions = {}

        self.phoneme_chains = {}
        self.word_length_distributions = {}

    def parse(self):
        count = 0
        total = sum(1 for line in self.pronouncing_dictionary)
        self.pronouncing_dictionary.seek(0)
        for line in self.pronouncing_dictionary:
            parsed_line = self._parse_word(line)
            self._increment_word_length_distributions_and_phoneme_chains(parsed_line)
            self._increment_stress_pattern_distributions_and_syllable_chains(parsed_line)
            count += 1
            if count % 10000 == 0:
                stdout.write('{} words out of {} parsed.\n'.format(count, total))
        self.pronouncing_dictionary.close()

        return self.words, self.phoneme_chains, self.word_length_distributions, \
            self.syllable_chains, self.stress_pattern_distributions

    def _parse_word(self, line):
        [word, word_pronunciation] = line.strip().split('\t')

        phonemes = {}
        phonemes['stressed'] = word_pronunciation.split()
        phonemes['unstressed'] = [destress(phoneme) for phoneme in phonemes['stressed']]

        for stressing in ['stressed', 'unstressed']:
            phonemes[stressing] = ['START_WORD'] + phonemes[stressing] + ['END_WORD']

        frequency = self.word_frequencies[word] if word in self.word_frequencies else 1

        self.words.append((word, word_pronunciation, frequency))

        return phonemes, frequency

    # pylint: disable=invalid-name
    def _increment_word_length_distributions_and_phoneme_chains(self, parsed_line):
        phonemes, frequency = parsed_line
        word_length = len(phonemes['stressed'])

        for weighting in OPTION_VALUES['weighting']:
            increment = 1 if weighting == 'unweighted' else frequency

            sparse(self.word_length_distributions.setdefault(weighting, []), word_length, 0)

            self.word_length_distributions[weighting][0] += increment
            self.word_length_distributions[weighting][word_length] += increment

            for stressing in OPTION_VALUES['stressing']:
                self.phoneme_chains.setdefault(weighting, {}).setdefault(stressing, [])
                word_length = len(phonemes[stressing])

                for word_position in range(0, word_length - 1):
                    phoneme = phonemes[stressing][word_position]
                    next_phoneme = phonemes[stressing][word_position + 1]

                    for ignore_length in [False, True]:
                        # the minus two is for start_word and end_word
                        length = 0 if ignore_length else word_length - 2
                        sparse(self.phoneme_chains[weighting][stressing], length, [])

                        for ignore_position in [False, True]:
                            # the plus 1 is because word_position is also 0-indexed
                            # but we need it to start in index 1 since 0 is reserved
                            # for the catch-all (btw, the index 1 has only one key, START_WORD)
                            position = 0 if ignore_position else word_position + 1
                            sparse(self.phoneme_chains[weighting][stressing][length], position, {})

                            self.phoneme_chains[weighting][stressing][length][position].\
                                setdefault(phoneme, {}).setdefault(next_phoneme, 0)
                            self.phoneme_chains[weighting][stressing][length][position]\
                                [phoneme][next_phoneme] += increment

    # pylint: disable=too-many-locals,line-too-long
    def _increment_stress_pattern_distributions_and_syllable_chains(self, parsed_line):
        phonemes, frequency = parsed_line
        phonemes = phonemes['stressed']
        syllables = parse_syllables(phonemes)
        syllable_length = len(syllables)

        stress_pattern = [stress_level(syllable) for syllable in syllables]
        tupled_stress_pattern = tuple(stress_pattern[1:-1])

        for weighting in OPTION_VALUES['weighting']:
            self.syllable_chains.setdefault(weighting, [])

            increment = 1 if weighting == 'unweighted' else frequency

            self.stress_pattern_distributions.setdefault(weighting, {}).setdefault(tupled_stress_pattern, 0)
            self.stress_pattern_distributions[weighting][tupled_stress_pattern] += increment

            for ignore_length in [False, True]:
                length = 0 if ignore_length else syllable_length - 2 # for syllables, only off by 1, bc start_word and end_word aren't each their own thing, but they are each halfway on one syllable so .5 + .5 = 1 ... except that now i forced start word to be its own syllable too... except since these are technically syllable transitions, an extra one because onto it then offof it
                sparse(self.syllable_chains[weighting], length, [])

                for syllable_position in range(0, syllable_length - 1):
                    syllable = syllables[syllable_position]
                    next_syllable = syllables[syllable_position + 1]

                    for ignore_position in [False, True]:
                        position = 0 if ignore_position else syllable_position + 1
                        sparse(self.syllable_chains[weighting][length], position, {})

                        for stressing in OPTION_VALUES['stressing']:
                            syllable_stress_level = 'ignore_stress' if stressing == 'unstressed' else stress_level(syllable)
                            next_syllable_stress_level = 'ignore_stress' if stressing == 'unstressed' else stress_level(next_syllable)
                            # so... you could unstress this syllable if you wanted to save a little space
                            # particularly it is confusing when under the 'ignore_stress' key...

                            self.syllable_chains[weighting][length][position].setdefault(syllable_stress_level, {})\
                                .setdefault(next_syllable_stress_level, {}).setdefault(syllable, {}).setdefault(next_syllable, 0)
                            self.syllable_chains[weighting][length][position][syllable_stress_level]\
                                [next_syllable_stress_level][syllable][next_syllable] += increment
# pylint: enable=too-many-locals,too-few-public-methods,invalid-name
