import random, sys, time, cPickle

with open('phoneme_probabilities.pkl', 'rb') as input:
    phoneme_chain_prob = cPickle.load(input)

def get_next_phoneme(current_phoneme, random_number):
    current_next_phoneme_chance = 2.0
    current_next_phoneme = ''
    for transition_phoneme, chance in phoneme_chain_prob[current_phoneme].iteritems():
        if chance >= random_number and chance < current_next_phoneme_chance:
            current_next_phoneme_chance = chance
            current_next_phoneme = transition_phoneme
    return current_next_phoneme

current_phoneme = 'START_WORD'
while True:
    next_phoneme = get_next_phoneme(current_phoneme, random.random())
    if next_phoneme == 'END_WORD':
        sys.stdout.write('\n')
        current_phoneme = 'START_WORD'
        time.sleep(.5)
    else:
        sys.stdout.write(next_phoneme + ' ')
        current_phoneme = next_phoneme
