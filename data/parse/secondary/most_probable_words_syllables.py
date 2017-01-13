from lib.options import MAX_WORD_LENGTH, POOL_MAX, option_value_string_to_boolean
from lib.score import get_score
from data.secondary_data_io import load

# pylint: disable=too-few-public-methods,no-self-use
class MostProbableWordsSyllables(object):
    def __init__(self, syllable_chains, length_consideration, options):
        positioning, self.stressing, self.weighting, self.scoring_method = options
        self.ignore_position = option_value_string_to_boolean(positioning)
        self.ignore_length = option_value_string_to_boolean(length_consideration)
        self.unstressed = option_value_string_to_boolean(self.stressing)

        self.stressing_patterns = [x[0] for x in load('stress_pattern_distributions')[self.weighting]]
        self.syllable_chains = syllable_chains

        self.count = 0
        self.most_probable_words = []

        default_limits = load('default_limits')
        self.limit = 1.0 if not default_limits else default_limits\
            .get(length_consideration, {}).get(positioning, {}).get(self.stressing, {})\
            .get(self.weighting, {}).get(self.scoring_method).get('use_syllables', 1.0)
        self.upper_limit = None
        self.lower_limit = None

        self.target_length = None

        self.syllable_bucket_errors = 0
        self.syllable_non_bucket_errors = 0

    def get(self):
        good_count = False
        while not good_count:
            self.most_probable_words = []
            self.count = 0

            if not self.unstressed:
                for stress_pattern in self.stressing_patterns:
                    self.target_length = len(stress_pattern) # interesting... this was nothing, and +1 did not affect the error counts....
                    self.stress_pattern = ['start_word'] + list(stress_pattern) + ['end_word']
                    self.get_next_syllable([tuple(['START_WORD'])], 1.0)
            elif self.unstressed:
                for target_length in range(1, max([len(x) for x in self.stressing_patterns])):
                    # dont happen to be words of this syllable length, 
                    # so even the 0 "ignore length" bucket was not populated
                    if len(self.syllable_chains[self.weighting][target_length]) > 0:
                        self.target_length = target_length
                        self.stress_pattern = ['ignore_stress'] * target_length + ['end_word']
                        self.get_next_syllable([tuple(['START_WORD'])], 1.0)

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

        # and we get 500 - 1000 syllable bucket errors whenever it is STRESSED
        if self.syllable_bucket_errors > 0:
            print 'error report!', self.syllable_bucket_errors, 'versus', self.syllable_non_bucket_errors

        self.most_probable_words.sort(key=lambda x: -x[1])
        return self.most_probable_words[:POOL_MAX], self.limit

    def get_next_syllable(self, word, score):
        self.count += 1
        if self.count > POOL_MAX * 10:
            return

        current_length = len(word)

        if current_length <= MAX_WORD_LENGTH:
            length_bucket = 0 if self.ignore_length else self.target_length
            position_bucket = 0 if self.ignore_position else current_length
            current_stress = self.stress_pattern[current_length - 1]
            next_stress = self.stress_pattern[current_length]
            current_syllable = word[current_length - 1]

            if self.unstressed and next_stress == 'end_word':
                # this one is a real thing maybe. syllable bucket error is def bad
                chosen_bucket = self.syllable_chains[self.weighting]\
                    [length_bucket]\
                    [position_bucket]\
                    [current_stress]\
                    ['ignore_stress']\
                    [current_syllable]
            elif current_syllable not in self.syllable_chains[self.weighting]\
                [length_bucket]\
                [position_bucket]\
                [current_stress]\
                [next_stress].keys():
                self.syllable_bucket_errors += 1
                # print 'syllable error bucket path', self.weighting, length_bucket, position_bucket, current_stress, next_stress, current_syllable
                chosen_bucket = None
            else:
                # this is proving how the proportion of ones without errors is 
                # not overwhelmingly large. it's like 20% of them are wrong, 
                # which is non-negligible, we have to figure this out
                self.syllable_non_bucket_errors += 1
                chosen_bucket = self.syllable_chains[self.weighting]\
                    [length_bucket]\
                    [position_bucket]\
                    [current_stress]\
                    [next_stress]\
                    [current_syllable]

            if chosen_bucket is not None:
                for next_syllable, probability in chosen_bucket.iteritems():
                    score = get_score(score, self.scoring_method, probability, current_length)
                    if score < self.limit:
                        pass
                    elif next_stress == 'end_word' or next_syllable[-1] == 'END_WORD':
                        afraid_word = word[1:] # this is always just start word. i tried switching things up so that we kick off "get" with an empty array but it got off and scary... try again in a separate commit
                        if next_syllable[-1] == 'END_WORD':
                            afraid_word.append(next_syllable[:-1])
                        else:
                            afraid_word.append(next_syllable)
                        stringified_word = [' '.join(syllable) for syllable in afraid_word]
                        stringified_word = ' '.join(stringified_word)
                        self.most_probable_words.append(
                            (stringified_word, score, current_length)
                        )
                    else:
                        grown_word = word[:]
                        grown_word.append(next_syllable)
                        self.get_next_syllable(grown_word, score)
# pylint: enable=too-few-public-methods,no-self-use
