import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from lib.type_conversion import array_to_string
from lib.score import get_score
from lib.options import SCORING_METHODS, DEFAULT_LIMITS, POOL_MAX, MAX_WORD_LENGTH, \
    option_value_boolean_to_string

# def diagnose_counts_helper(options):
#     output = ''
#     output += 'ignore_position ' if options[0] else 'use_pos '
#     output += 'unstressed ' if options[1] else 'stressed '
#     output += 'unweighted ' if options[2] else 'weighted '
#     output += 'avg ' if options[3] else 'integral '
#     output += '+' if options[4] else '*'
#     return output

# comments are useful for finding the right threshold for the search

# pylint: disable=too-many-instance-attributes
class MostProbableWords(object):
    def __init__(self, word_lengths, ignore_length, options):
        ignore_position, unstressed, unweighted, method_mean, method_addition = options
        length_consideration = option_value_boolean_to_string('length_consideration', ignore_length)
        positioning = option_value_boolean_to_string('positioning', ignore_position)
        stressing = option_value_boolean_to_string('stressing', unstressed)
        weighting = option_value_boolean_to_string('weighting', unweighted)

        self.most_probable_words = []
        self.word_lengths = word_lengths[weighting][stressing]
        self.scoring_method = SCORING_METHODS.keys()[
            SCORING_METHODS.values().index((method_mean, method_addition))
        ]
        self.ignore_position = ignore_position
        self.ignore_length = ignore_length
        self.limit = DEFAULT_LIMITS[length_consideration][positioning]\
            [stressing][weighting][self.scoring_method]
        self.count = 0
        self.word_length = None
        # print length_consideration, diagnose_counts_helper(options), 'limit', self.limit

    def get(self):
        if self.ignore_length:
            self.word_length = 0
            self.get_next_phoneme(['START_WORD'], 1.0)
        else:
            for word_length in range(1, len(self.word_lengths)):
                self.word_length = word_length
                if len(self.word_lengths[self.word_length]) != 0:
                    self.get_next_phoneme(['START_WORD'], 1.0)

        self.most_probable_words.sort(key=lambda x: -x[1])

        # print 'total words searched: ', self.count
        # print 'total words qualified: ', len(self.most_probable_words), '\n'

        return self.most_probable_words[:POOL_MAX]

    def get_next_phoneme(self, word, score):
        self.count += 1
        word_length = len(word)
        current_phoneme = word[word_length - 1]

        if word_length > MAX_WORD_LENGTH:
            pass
        else:
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
