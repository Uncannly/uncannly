import random, time, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import file

phoneme_chain_prob = file.load('phoneme_probabilities')
phonetic_words = file.load('phonetic_words')
words = file.load('words')

def get_next_phoneme(current_phoneme, random_number):
    current_next_phoneme_chance = 2.0
    current_next_phoneme = ''
    for transition_phoneme, chance in phoneme_chain_prob[current_phoneme].iteritems():
        if chance >= random_number and chance < current_next_phoneme_chance:
            current_next_phoneme_chance = chance
            current_next_phoneme = transition_phoneme
    return current_next_phoneme

def not_in_dict(word):
    if word in phonetic_words:
        index = phonetic_words.index(word)
        print '{} (word exists already: {})'.format(word, words[index])
        return False
    else:
        return True

word_to_output = ''
current_phoneme = 'START_WORD'
while True:
    next_phoneme = get_next_phoneme(current_phoneme, random.random())
    if next_phoneme == 'END_WORD':
        if not_in_dict(word_to_output):
            print word_to_output
        word_to_output = ''
        current_phoneme = 'START_WORD'
        time.sleep(.5)
    else:
        word_to_output = next_phoneme if len(word_to_output) == 0 else word_to_output + ' ' + next_phoneme
        current_phoneme = next_phoneme
