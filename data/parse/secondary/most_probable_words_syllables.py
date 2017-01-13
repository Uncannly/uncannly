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

    def get(self):
        # return [('AH2 AH0 AH1 AH0 AH0', 0.08, 5)] * 500, 0.005
        good_count = False
        while not good_count:
            self.most_probable_words = []
            self.count = 0

            # stressed
            if not self.unstressed:
                for stress_pattern in self.stressing_patterns:
                    # self.word_length = word_length
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

            good_count = True

        # print 'wooooo', self.most_probable_words[:POOL_MAX]
        # raw_input()
        return self.most_probable_words[:POOL_MAX], self.limit

    def get_next_syllable(self, word, score):
        # print self.count, 'versus max', POOL_MAX * 10
        self.count += 1
        if self.count > POOL_MAX * 10:
            # print 'ABORT!!! too deep'
            return

        current_length = len(word)
        # current_syllable = tuple([word[current_length - 1]])
        current_syllable = word[current_length - 1]

        if current_length > MAX_WORD_LENGTH:
            # print 'hit the max word length, ABORT!! TOO LONG'
            pass
        else:
            # word_position = 0 if self.ignore_position else current_length
            length = 0 if self.ignore_length else self.length
            # next_syllables = self.syllable_chains[self.weighting][length][position]
            # for next_syllable, probability in next_syllables[current_syllable]:
            #     pass

            syllable_length = len(self.stress_pattern)
            length_bucket = 0 if self.ignore_length else syllable_length - 2

            # for current_length in range(0, syllable_length - 1):
            position_bucket = 0 if self.ignore_position else current_length # + 1
            if position_bucket > len(self.syllable_chains[self.weighting][length_bucket]):
                position_bucket = 0
                # print 'i dont quite understand why this is happening or this solution'

            # print 'whats up with stress pattern, why would it be empty?'
            # if len(self.stress_pattern) > 0: # i think this means not ignore stress
            current_stress = self.stress_pattern[current_length - 1]
            # else:
            #     current_stress = 'ignore_stress'
            # print 'trying to figure out why this would blow up, cur len is', current_length, 'and sress pattern is ', self.stress_pattern
            next_stress = self.stress_pattern[current_length]

            # odsijagoisaoigsoigj
            # if the stress pattern is only one entry of ignore stress, then do something
            # because on line 130 the way it ends anyway is to see end word and that does not even exist for unstressed mode

            # print 'why can i not find you', current_syllable, 'in', 
            # for thing in self.syllable_chains[self.weighting]\
            #     [length_bucket]\
            #     [position_bucket]\
            #     [current_stress]\
            #     [next_stress]:
            #     print thing
            #     raw_input()

            # print 'bucket path', self.weighting, length_bucket, position_bucket, current_stress, next_stress, current_syllable
            # print 'contents', self.syllable_chains[self.weighting]\
            #     [length_bucket]\
            #    [position_bucket]\
            #    [current_stress].keys()
            if self.unstressed and next_stress == 'end_word':
                chosen_bucket = self.syllable_chains[self.weighting]\
                    [length_bucket]\
                   [position_bucket]\
                   [current_stress]\
                   ['ignore_stress']\
                   [current_syllable]
            else:
                if position_bucket > len(self.syllable_chains[self.weighting][length_bucket]):
                    # print 'oaky it happened, wtf??', position_bucket, len(self.syllable_chains[self.weighting][length_bucket])
                    # raw_input()
                    chosen_bucket = self.syllable_chains[self.weighting]\
                        [length_bucket]\
                       [0]\
                       [current_stress]\
                       [next_stress]\
                       [current_syllable]
                elif length_bucket >= 10 and position_bucket == 0:
                    # print 'i reallllllllly odnt get what is happeneing' # but it appears you CAN go higher, its just that sometimes a length is totally missing anything inside it....
                    # raw_input()
                    chosen_bucket = self.syllable_chains[self.weighting]\
                        [0]\
                       [0]\
                       [current_stress]\
                       [next_stress]\
                       [current_syllable]  
                else:
                    if current_syllable not in self.syllable_chains[self.weighting]\
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
                        chosen_bucket = None
                    else:
                        chosen_bucket = self.syllable_chains[self.weighting]\
                            [length_bucket]\
                           [position_bucket]\
                           [current_stress]\
                           [next_stress]\
                           [current_syllable]

                # if self.syllable is None:
                #     syllable_bucket = chosen_bucket[tuple(['START_WORD'])]
                # else:
                #     syllable_bucket = chosen_bucket.get(self.syllable, None)

                # if syllable_bucket is None:
                #     # word = ['This shouldnt happen but we couldnt connect buckets']
                #     self.word = []
                #     break
            # print 'alright, bout to iterate over these iteritmes in this bucket', chosen_bucket.keys()
            if chosen_bucket is None:
                pass
            else:
                for next_syllable, probability in chosen_bucket.iteritems():
                    # print 'this syllable is', next_syllable, 'probability', probability
                    score = get_score(score, self.scoring_method, probability, current_length)
                    # print 'came up with score', score
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
                        stringified_word = [' '.join(syllable) for syllable in afraid_word] # array_to_string(word[1:len(word)])# 
                        # stringified_word = stringified_word[:-1] # yeah this is bad, i am dropping the last thing
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
