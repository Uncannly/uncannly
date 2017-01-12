from lib.options import MAX_WORD_LENGTH, POOL_MAX, option_value_string_to_boolean
from data.secondary_data_io import load

# pylint: disable=too-few-public-methods,no-self-use
class MostProbableWordsSyllables(object):
    def __init__(self, syllable_chains, length_consideration, options):
        positioning, stressing, self.weighting, self.scoring_method = options
        self.ignore_position = option_value_string_to_boolean(positioning)
        self.ignore_length = option_value_string_to_boolean(length_consideration)

        default_limits = load('default_limits')

        self.most_probable_words = []
        self.stressing_patterns = [x[0] for x in load('stress_pattern_distributions')[self.weighting]]
        self.count = 0
        self.syllable_chains = syllable_chains
        self.limit = 1.0 if not default_limits else default_limits\
            .get(length_consideration, {}).get(positioning, {}).get(stressing, {})\
            .get(self.weighting, {}).get(self.scoring_method).get('use_syllables', 1.0)

    def get(self):
        # return [('AH2 AH0 AH1 AH0 AH0', 0.08, 5)] * 500, 0.005
        good_count = False
        while not good_count:
            self.most_probable_words = []
            self.count = 0

            # stressed
            for stressing_pattern in self.stressing_patterns:
                # self.word_length = word_length
                self.stressing_pattern = stressing_pattern
                self.length = len(stressing_pattern)
                # print 'stressing pattern', self.stressing_pattern
                self.get_next_syllable([], 1.0)

            # unstressed
            for length in range(0, max([len(x) for x in self.stressing_patterns])):
                self.stressing_pattern = ['ignore_stress'] * length
                self.length = length
                # print 'lengths', self.stressing_pattern
                self.get_next_syllable([], 1.0)

            good_count = True

        return self.most_probable_words[:POOL_MAX], self.limit

    def get_next_syllable(self, word, score):
        self.count += 1
        if self.count > POOL_MAX * 10:
            return

        word_length = len(word)
        # current_syllable = word[word_length - 1]

        if word_length > MAX_WORD_LENGTH:
            pass
        else:
            word_position = 0 if self.ignore_position else word_length
            length = 0 if self.ignore_length else self.length
            # next_syllables = self.syllable_chains[self.weighting][length][position]
            # for next_syllable, probability in next_syllables[current_syllable]:
            #     pass
# pylint: enable=too-few-public-methods,no-self-use
