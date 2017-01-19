from data.secondary_data_io import load
from lib.conversion import array_to_string
from lib.score import get_score, update_limits
from lib.options import POOL_MAX, MAX_WORD_LENGTH, option_value_string_to_boolean, \
    option_value_boolean_to_string
from lib.ipa import clean_end_word_pseudovowel

class MostProbableWords(object):
    def __init__(self, chains, options):
        positioning, self.stressing, self.weighting, self.scoring_method, \
            length_consideration, self.ignore_syllables = options
        self.ignore_position = option_value_string_to_boolean(positioning)
        self.ignore_length = option_value_string_to_boolean(length_consideration)
        self.unstressed = option_value_string_to_boolean(self.stressing)
        syllable_use = option_value_boolean_to_string('syllable_use', self.ignore_syllables)

        default_limits = load('default_limits')
        self.limit = 1.0 if not default_limits else default_limits\
            .get(length_consideration, {}).get(positioning, {}).get(self.stressing, {})\
            .get(self.weighting, {}).get(self.scoring_method).get(syllable_use, 1.0)
        self.upper_limit = None
        self.lower_limit = None

        self.most_probable_words = []
        self.count = 0

        self.chains = chains[self.weighting][self.stressing] if self.ignore_syllables else chains

        self.target_length = None

        if not self.ignore_syllables:
            self.stressing_patterns = \
                [x[0] for x in load('stress_pattern_distributions')[self.weighting]]

    def get(self):
        good_count = False
        while not good_count:
            self.most_probable_words = []
            self.count = 0

            if self.ignore_syllables:
                if self.ignore_length:
                    self.target_length = 0
                    self._get_next_unit(['START_WORD'], 1.0)
                else:
                    for target_length in range(1, len(self.chains)):
                        self.target_length = target_length
                        if len(self.chains[self.target_length]) != 0:
                            self._get_next_unit(['START_WORD'], 1.0)

            else:
                if not self.unstressed:
                    for stress_pattern in self.stressing_patterns:
                        self.target_length = len(stress_pattern)
                        self.stress_pattern = ['start_word'] + list(stress_pattern) + ['end_word']
                        self._get_next_unit([tuple(['START_WORD'])], 1.0)
                else:
                    for target_length in range(1, max([len(x) for x in self.stressing_patterns])):
                        # dont happen to be words of this syllable length,
                        # so even the 0 "ignore length" bucket was not populated
                        if len(self.chains[self.weighting][target_length]) > 0:
                            self.target_length = target_length
                            self.stress_pattern = ['ignore_stress'] * target_length + ['end_word']
                            self._get_next_unit([tuple(['START_WORD'])], 1.0)

            # print 'total words searched: ', self.count
            # print 'total words qualified: ', len(self.most_probable_words)

            good_count, self.limit, self.lower_limit, self.upper_limit = \
                update_limits(len(self.most_probable_words),
                              self.limit, self.lower_limit, self.upper_limit)

        self.most_probable_words.sort(key=lambda x: -x[1])
        return self.most_probable_words[:POOL_MAX], self.limit

    def _get_next_unit(self, word, score):
        self.count += 1
        if self.count > POOL_MAX * 10:
            return

        current_length = len(word)
        if current_length > MAX_WORD_LENGTH:
            return

        current_unit = word[-1]
        position = 0 if self.ignore_position else current_length

        if self.ignore_syllables:
            next_units = self.chains[self.target_length][position][current_unit]
        else:
            length = 0 if self.ignore_length else self.target_length
            current_stress = self.stress_pattern[current_length - 1]
            next_stress = self.stress_pattern[current_length]

            if self.unstressed and next_stress == 'end_word':
                next_units = self.chains[self.weighting]\
                    [length]\
                    [position]\
                    [current_stress]\
                    ['ignore_stress']\
                    [current_unit].iteritems()
            elif current_unit not in self.chains[self.weighting]\
                [length]\
                [position]\
                [current_stress]\
                [next_stress].keys():
                next_units = None
                # this is because the syllable chosen, while it of course exists
                # in the first stress level, may not happen to exist for the transition
                # from that stress level to the next one in the given stressing pattern
            else:
                next_units = self.chains[self.weighting]\
                    [length]\
                    [position]\
                    [current_stress]\
                    [next_stress]\
                    [current_unit].iteritems()

        if next_units is None:
            return

        for next_unit, probability in next_units:
            score = get_score(score, self.scoring_method, probability, current_length)
            if score < self.limit:
                pass
            elif self.ignore_syllables and next_unit == 'END_WORD':
                stringified_word = array_to_string(word[1:len(word)])
                self.most_probable_words.append(
                    (stringified_word, score, self.target_length))
            elif not self.ignore_syllables and (next_stress == 'end_word' or next_unit[-1] == 'END_WORD'):
                afraid_word = word[1:]
                # this is always just start word. i tried switching things up
                # so that we kick off "get" with an empty array but it
                # got off and scary... try again in a separate commit
                syllable = clean_end_word_pseudovowel(next_unit)
                if syllable:
                    afraid_word.append(syllable)
                self.most_probable_words.append(
                    (afraid_word, score, current_length))
            else:
                grown_word = word[:]
                grown_word.append(next_unit)
                self._get_next_unit(grown_word, score)
