import json, sys, time, cPickle

words = []
phonetic_words = []

phoneme_chain_absolute = {}
phoneme_chain_prob = {}
ranked_most_likely_next_phonemes_per_phoneme = {}

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

f = open('primary_data/unlemmatized_frequency_list.txt', 'r')
for line in f:
		split_by_tabs = line.strip().split(' ')
		freq = split_by_tabs[0]
		word = split_by_tabs[1].upper()
		word_freqs[word] = freq
f.close()

f = open('primary_data/cmu_pronouncing_dictionary.txt', 'r')
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

for phoneme, potential_next_phonemes in phoneme_chain_absolute.iteritems():

    total_occurrences_of_next_phonemes = 0.0
    for _, num in potential_next_phonemes.iteritems():
        total_occurrences_of_next_phonemes += num

    stacked_phoneme_probabability_thresholds = {}

    phoneme_probabibilies = {}

    upper_threshold_for_this_phoneme_in_range = 0.0
    for potential_next_phoneme, num in potential_next_phonemes.iteritems():
    		chance_of_this_phoneme = num / total_occurrences_of_next_phonemes

    		phoneme_probabibilies[chance_of_this_phoneme] = potential_next_phoneme

    		upper_threshold_for_this_phoneme_in_range += chance_of_this_phoneme

    		stacked_phoneme_probabability_thresholds[potential_next_phoneme] = upper_threshold_for_this_phoneme_in_range

    phoneme_chain_prob[phoneme] = stacked_phoneme_probabability_thresholds

    chances = []
    for chance, potential_next_phoneme in phoneme_probabibilies.iteritems():
    		chances.append(chance)
    chances.sort(reverse=True)

    ranked_most_likely_next_phonemes = []
    for chance in chances:
    		ranked_most_likely_next_phonemes.append(phoneme_probabibilies[chance])

    ranked_most_likely_next_phonemes_per_phoneme[phoneme] = ranked_most_likely_next_phonemes

with open('secondary_data/phoneme_probabilities.pkl', 'wb') as output:
    cPickle.dump(phoneme_chain_prob, output, -1)

with open('secondary_data/phonetic_words.pkl', 'wb') as output:
    cPickle.dump(phonetic_words, output, -1)

with open('secondary_data/words.pkl', 'wb') as output:
    cPickle.dump(words, output, -1)

with open('secondary_data/ranked_most_likely_next_phonemes_per_phoneme.pkl', 'wb') as output:
    cPickle.dump(ranked_most_likely_next_phonemes_per_phoneme, output, -1)