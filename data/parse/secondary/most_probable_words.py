import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..', '..'))

from lib.type_conversion import array_to_string
from lib.score import get_score
from lib.options import booleans_to_strings, SCORING_METHODS, DEFAULT_LIMITS, POOL_MAX

# def diagnose_counts_helper(options):
#     output = ''
#     output += 'ignore_position ' if options[0] else 'use_pos '
#     output += 'unstressed ' if options[1] else 'stressed '
#     output += 'unweighted ' if options[2] else 'weighted '
#     output += 'avg ' if options[3] else 'integral '
#     output += '+' if options[4] else '*'
#     return output 

# comments are useful for finding the right threshold for the search
class MostProbableWords(object):
    def __init__(self, word_positions, options):
        ignore_position, unstressed, unweighted, method_mean, method_addition = options
        stressing, weighting = booleans_to_strings(unstressed, unweighted)
        positioning = 'ignore_position' if ignore_position else 'use_position'

        self.most_probable_words = []
        self.word_positions = word_positions
        self.scoring_method = SCORING_METHODS.keys()[
            SCORING_METHODS.values().index((method_mean, method_addition))
        ]
        self.ignore_position = ignore_position
        self.limit = DEFAULT_LIMITS[positioning][stressing][weighting][self.scoring_method]
        self.count = 0
        # print diagnose_counts_helper(options), 'limit', self.limit

    def get(self):
        self.get_next_phoneme(['START_WORD'], 1.0)
        self.most_probable_words.sort(key=lambda x: -x[1])

        # print 'total words searched: ', self.count
        # print 'total words qualified: ', len(self.most_probable_words), '\n'

        return self.most_probable_words[:POOL_MAX]

    def get_next_phoneme(self, word, score):
        self.count += 1
        word_length = len(word)
        current_phoneme = word[word_length - 1]

        if word_length > 20:
            pass
        else:
            i = 0 if self.ignore_position else word_length
            next_phonemes = self.word_positions[i]
            for next_phoneme, probability in next_phonemes[current_phoneme]:
                score = get_score(score, self.scoring_method, probability, word_length)
                if score < self.limit:
                    pass
                elif next_phoneme == 'END_WORD':
                    stringified_word = array_to_string(word[1:len(word)])
                    self.most_probable_words.append((stringified_word, score))
                else:
                    grown_word = word[:]
                    grown_word.append(next_phoneme)
                    self.get_next_phoneme(grown_word, score)
