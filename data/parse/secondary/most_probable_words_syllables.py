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

        default_limits = load('default_limits')

        self.most_probable_words = []
        self.stressing_patterns = [x[0] for x in load('stress_pattern_distributions')[self.weighting]]
        self.count = 0
        self.syllable_chains = syllable_chains
        self.limit = 1.0 if not default_limits else default_limits\
            .get(length_consideration, {}).get(positioning, {}).get(self.stressing, {})\
            .get(self.weighting, {}).get(self.scoring_method).get('use_syllables', 1.0)

        self.upper_limit = None
        self.lower_limit = None

        # self.position_bucket_errors = 0 # cool these have stopped happening
        self.length_bucket_errors = 0
        self.syllable_bucket_errors = 0

    def get(self):
        good_count = False
        while not good_count:
            self.most_probable_words = []
            self.count = 0

            # stressed
            if not self.unstressed:
                for stress_pattern in self.stressing_patterns:
                    self.length = len(stress_pattern)

                    self.stress_pattern = ['start_word'] + list(stress_pattern) + ['end_word']

                    # print 'about to do everything for stressing pattern', self.stress_pattern
                    self.get_next_syllable([tuple(['START_WORD'])], 1.0)

            # unstressed
            elif self.unstressed:
                for length in range(1, max([len(x) for x in self.stressing_patterns])):
                    self.length = length

                    self.stress_pattern = ['ignore_stress'] * length
                    self.stress_pattern = list(self.stress_pattern) + ['end_word']
                    # print 'about to do everything for unstressed pattern of length', self.stress_pattern
                    self.get_next_syllable([tuple(['START_WORD'])], 1.0)


            if len(self.most_probable_words) < POOL_MAX:
                self.upper_limit = self.limit
                print 'gotta lower limit', self.limit
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
                print 'gotta raise limit', self.limit
                self.lower_limit = self.limit
                if self.upper_limit:
                    self.limit += (self.upper_limit - self.limit) / 2
                else:
                    self.limit *= 2
            else:
                good_count = True

        # okay cool, so we get TWO length bucket errors whenever it is USE LENGTH but UNSTRESSED
        # and that seems to only happen when it is length 10 or 11, so my current theory is that there is jus a gap in syllable counts here, like antidis- and supercalli- are both 12 and the next highest is 9. so just need to actually deal with that situation. instead of setting to 0, just skip that length. do as separate commit.
        # and we get 500 - 1000 syllable bucket errors whenever it is STRESSED
        print 'error report!', self.length_bucket_errors, self.syllable_bucket_errors

        self.most_probable_words.sort(key=lambda x: -x[1])

        return self.most_probable_words[:POOL_MAX], self.limit

    def get_next_syllable(self, word, score):
        self.count += 1
        if self.count > POOL_MAX * 10:
            return

        current_length = len(word)
        current_syllable = word[current_length - 1]

        if current_length > MAX_WORD_LENGTH:
            pass
        else:
            length = 0 if self.ignore_length else self.length
            syllable_length = len(self.stress_pattern)
            length_bucket = 0 if self.ignore_length else syllable_length - 2

            current_stress = self.stress_pattern[current_length - 1]
            next_stress = self.stress_pattern[current_length]

            position_bucket = 0 if self.ignore_position else current_length # + 1
            if position_bucket > len(self.syllable_chains[self.weighting][length_bucket]):
                position_bucket = 0
                print 'i dont quite understand why this is happening or this solution'
                print 'position error bucket path', self.weighting, length_bucket, position_bucket, current_stress, next_stress, current_syllable

            # print 'contents', self.syllable_chains[self.weighting]\
            if len(self.syllable_chains[self.weighting][length_bucket]) == 0: # length_bucket >= 10 and position_bucket == 0:
                # print 'i reallllllllly odnt get what is happeneing' # but it appears you CAN go higher, its just that sometimes a length is totally missing anything inside it....
                # raw_input()
                # chosen_bucket = self.syllable_chains[self.weighting]\
                #     [0]\
                #    [position_bucket]\
                #    [current_stress]\
                #    [next_stress]\
                #    [current_syllable]
                self.length_bucket_errors += 1
                print 'length error bucket path', self.weighting, length_bucket, position_bucket, current_stress, next_stress, current_syllable
                chosen_bucket = None 
            elif self.unstressed and next_stress == 'end_word': # this one is maybe a real thing. others are just oopses
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
                # print 'how often is it not in keys?'
                # print   self.syllable_chains[self.weighting]\
                #     [length_bucket]\
                #    [position_bucket]\
                #    [current_stress]\
                #    [next_stress].keys()
                # raw_input()
                self.syllable_bucket_errors += 1
                chosen_bucket = None
            else:
                chosen_bucket = self.syllable_chains[self.weighting]\
                    [length_bucket]\
                   [position_bucket]\
                   [current_stress]\
                   [next_stress]\
                   [current_syllable]

            # print 'alright, bout to iterate over these iteritmes in this bucket', chosen_bucket.keys()
            if chosen_bucket is None:
                pass
            else:
                for next_syllable, probability in chosen_bucket.iteritems():
                    # print 'this syllable is', next_syllable, 'probability', probability
                    score = get_score(score, self.scoring_method, probability, current_length)
                    if score < self.limit:
                        # print 'over the limit', score, self.limit
                        pass
                    elif next_stress == 'end_word' or next_syllable[-1] == 'END_WORD':
                        # print 'ended on syllable', next_syllable
                        afraid_word = word[1:]
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
                        # print 'recursive callllll'
                        grown_word = word[:]
                        grown_word.append(next_syllable)
                        self.get_next_syllable(grown_word, score)
# pylint: enable=too-few-public-methods,no-self-use
