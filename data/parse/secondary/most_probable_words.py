from data.secondary_data_io import load
from lib.score import get_score, update_limits
from lib.options import POOL_MAX, MAX_WORD_LENGTH, option_value_string_to_boolean, \
    option_value_boolean_to_string
from lib.ipa import clean_end_word_pseudovowel
from lib.conversion import prepare_pattern

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

        self.chains = chains[self.weighting]

        self.target_length = None
        self.patterns = self._neutral_patterns() if self.ignore_syllables \
            else self._stress_patterns()

    def get(self):
        good_count = False
        while not good_count:
            self.most_probable_words = []
            self.count = 0

            for pattern in self.patterns:
                self.target_length = len(pattern)
                if self._pattern_is_not_empty():
                    self.pattern = prepare_pattern(pattern, self.unstressed, self.ignore_syllables)
                    self._get_next_unit(word=[], score=1.0)

            # print 'total words searched: ', self.count
            # print 'total words qualified: ', len(self.most_probable_words)

            good_count, self.limit, self.lower_limit, self.upper_limit = \
                update_limits(len(self.most_probable_words),
                              self.limit, self.lower_limit, self.upper_limit)

        self.most_probable_words.sort(key=lambda x: -x[1])
        return self.most_probable_words[:POOL_MAX], self.limit

    def _neutral_patterns(self):
        return [[None] * _ for _ in range(1, len(self.chains[self.stressing]))]

    def _stress_patterns(self):
        return [_[0] for _ in load('stress_pattern_distributions')[self.weighting]]

    def _pattern_is_not_empty(self):
        return len(self._pattern_pather()) > 0

    def _pattern_pather(self):
        if self.ignore_syllables:
            return self.chains[self.stressing][self.target_length]
        return self.chains[self.target_length]

    def _get_next_unit(self, word, score):
        self.count += 1
        if self.count > POOL_MAX * 10:
            return

        current_position = len(word) + 1
        if current_position > MAX_WORD_LENGTH or current_position > self.target_length + 1:
            return

        next_units = self._get_next_units(word, current_position)
        if next_units is None:
            return

        for next_unit, probability in next_units:
            score = get_score(score, self.scoring_method, probability, current_position)
            if score > self.limit:
                next_step = self._save_word if self._finished(next_unit) else self._get_next_unit
                next_step(self._grow_word(word, next_unit), score)

    def _get_next_units(self, word, current_position):
        current_unit = self._get_current_unit(word, current_position)

        position = 0 if self.ignore_position else current_position
        length = 0 if self.ignore_length else self.target_length

        if self.ignore_syllables:
            return self.chains[self.stressing][length][position][current_unit]

        current_stress = self.pattern[current_position - 1]
        next_stress = self.pattern[current_position]

        if current_unit not in self.chains[length][position][current_stress][next_stress].keys():
            return None

        return self.chains[length][position][current_stress][next_stress][current_unit].iteritems()

    def _get_current_unit(self, word, current_position):
        if current_position > 1:
            return word[-1]
        return 'START_WORD' if self.ignore_syllables else tuple(['START_WORD'])

    def _grow_word(self, word, next_unit):
        grown_word = word[:]

        next_unit = clean_end_word_pseudovowel(next_unit, self.ignore_syllables)
        if next_unit:
            grown_word.append(next_unit)

        return grown_word

    def _finished(self, next_unit):
        return next_unit == 'END_WORD' or next_unit[-1] == 'END_WORD'

    def _save_word(self, word, score):
        self.most_probable_words.append((word, score, self.target_length))
