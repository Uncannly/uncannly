import json, sys, time, cPickle

words = []
phonetic_words = []

phoneme_chain_absolute = {}
phoneme_chain_prob = {}

word_freqs = {}

def store_phoneme_transition_instance(freq, first_phoneme, second_phoneme):
    if first_phoneme not in phoneme_chain_absolute:
        phoneme_chain_absolute[first_phoneme] = {}
    if second_phoneme not in phoneme_chain_absolute[first_phoneme]:
        phoneme_chain_absolute[first_phoneme][second_phoneme] = freq
    else:
        phoneme_chain_absolute[first_phoneme][second_phoneme] += freq

def store_phonemes_for_word(freq, phonetic_word):
    phonemes = phonetic_word.split()
    for i in range(0, len(phonemes)):
        phonemes[i] = phonemes[i].strip('012')
    phonetic_words.append(" ".join(phonemes))
    phonemes.insert(0, 'START_WORD')
    phonemes.append('END_WORD')
    for i in range(0, len(phonemes) - 1):
        store_phoneme_transition_instance(freq, phonemes[i], phonemes[i + 1])

f = open('unlemmatized_frequency_list.txt', 'r')
for line in f:
		split_by_tabs = line.strip().split(' ')
		freq = split_by_tabs[0]
		word = split_by_tabs[1].upper()
		word_freqs[word] = freq
f.close()

f = open('cmu_pronouncing_dictionary.txt', 'r')
for line in f:
    split_by_tabs = line.strip().split('\t')
    word = split_by_tabs[0]

    if (word in word_freqs):
    	freq = float(word_freqs[word]) 
    else:
    	freq = 1.0

    words.append(word)
    phonetic_word = split_by_tabs[1]
    store_phonemes_for_word(freq, phonetic_word)
f.close()

for phoneme, phoneme_transition_list in phoneme_chain_absolute.iteritems():
    num_occurrences = 0.0
    for transition_phoneme, num in phoneme_transition_list.iteritems():
        num_occurrences += num
    phoneme_chance_list = {}
    previous_chance = 0.0
    for transition_phoneme, num in phoneme_transition_list.iteritems():
        previous_chance += num / num_occurrences
        phoneme_chance_list[transition_phoneme] = previous_chance
    phoneme_chain_prob[phoneme] = phoneme_chance_list

with open('phoneme_probabilities.pkl', 'wb') as output:
    cPickle.dump(phoneme_chain_prob, output, -1)

with open('phonetic_words.pkl', 'wb') as output:
    cPickle.dump(phonetic_words, output, -1)

with open('words.pkl', 'wb') as output:
    cPickle.dump(words, output, -1)