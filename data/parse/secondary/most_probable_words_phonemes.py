from data.secondary_data_io import load
from lib.conversion import array_to_string
from lib.score import get_score
from lib.options import POOL_MAX, MAX_WORD_LENGTH, option_value_string_to_boolean

# pylint: disable=too-many-instance-attributes
class MostProbableWordsPhonemes(object):
    def __init__(self, word_lengths, length_consideration, options):
        positioning, stressing, weighting, self.scoring_method = options

        default_limits = load('default_limits')

        self.most_probable_words = []
        self.word_lengths = word_lengths[weighting][stressing]
        self.ignore_position = option_value_string_to_boolean(positioning)
        self.ignore_length = option_value_string_to_boolean(length_consideration)
        self.limit = 1.0 if not default_limits else default_limits\
            .get(length_consideration, {}).get(positioning, {}).get(stressing, {})\
            .get(weighting, {}).get(self.scoring_method).get('ignore_syllables', 1.0)
        if self.limit == 0:
            self.limit = 1.0
        self.upper_limit = None
        self.lower_limit = None
        self.count = 0
        self.word_length = None

    # pylint: disable=too-many-branches
    def get(self):
        good_count = False
        while not good_count:
            self.most_probable_words = []
            self.count = 0
            if self.ignore_length:
                self.word_length = 0
                self.get_next_phoneme(['START_WORD'], 1.0)
            else:
                for word_length in range(1, len(self.word_lengths)):
                    self.word_length = word_length
                    if len(self.word_lengths[self.word_length]) != 0:
                        self.get_next_phoneme(['START_WORD'], 1.0)

            # print 'total words searched: ', self.count
            # print 'total words qualified: ', len(self.most_probable_words)

            if len(self.most_probable_words) < POOL_MAX:
                self.upper_limit = self.limit
                if self.lower_limit:
                    self.limit -= (self.limit - self.lower_limit) / 2
                else:
                    self.limit /= 2

                if self.limit == 0:
                    print (
                        'With these parameters, it is not possible '
                        'to find enough words to meet the pool max.'
                    )
                    good_count = True
            elif len(self.most_probable_words) > POOL_MAX * 10:
                self.lower_limit = self.limit
                if self.upper_limit:
                    self.limit += (self.upper_limit - self.limit) / 2
                else:
                    self.limit *= 2
            else:
                good_count = True

        self.most_probable_words.sort(key=lambda x: -x[1])

        return self.most_probable_words[:POOL_MAX], self.limit
    # pylint: enable=too-many-branches

    def get_next_phoneme(self, word, score):
        self.count += 1
        if self.count > POOL_MAX * 10:
            return

        word_length = len(word)
        current_phoneme = word[word_length - 1]

        if word_length <= MAX_WORD_LENGTH:
            word_position = 0 if self.ignore_position else word_length
            next_phonemes = self.word_lengths[self.word_length][word_position]
            for next_phoneme, probability in next_phonemes[current_phoneme]:
                score = get_score(score, self.scoring_method, probability, word_length)
                if score < self.limit:
                    pass
                elif next_phoneme == 'END_WORD':
                    stringified_word = array_to_string(word[1:len(word)])
                    self.most_probable_words.append(
                        (stringified_word, score, self.word_length)
                    )
                else:
                    grown_word = word[:]
                    grown_word.append(next_phoneme)
                    self.get_next_phoneme(grown_word, score)
# pylint: enable=too-many-instance-attributes
