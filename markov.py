import json

phoneme_chain_absolute = {}
phoneme_chain_prob = {}

def store_phoneme_transition_instance(first_phoneme, second_phoneme):
    if first_phoneme not in phoneme_chain_absolute:
        phoneme_chain_absolute[first_phoneme] = {}
    if second_phoneme not in phoneme_chain_absolute[first_phoneme]:
        phoneme_chain_absolute[first_phoneme][second_phoneme] = 1.0
    else:
        phoneme_chain_absolute[first_phoneme][second_phoneme] += 1.0

def store_phonemes_for_word(phonetic_word):
    phonemes = phonetic_word.split()
    phonemes.insert(0, 'START_WORD')
    phonemes.append('END_WORD')
    for i in range(0, len(phonemes) - 1):
        store_phoneme_transition_instance(phonemes[i], phonemes[i + 1])

f = open('phoneticphonetic.txt', 'r')
for line in f:
    split_by_tabs = line.strip().split('\t')
    phonetic_word = split_by_tabs[1]
    store_phonemes_for_word(phonetic_word)
f.close()

for phoneme, phoneme_transition_list in phoneme_chain_absolute.iteritems():
    num_occurrences = 0.0
    for transition_phoneme, num in phoneme_transition_list.iteritems():
        num_occurrences += num
    phoneme_chance_list = {}
    for transition_phoneme, num in phoneme_transition_list.iteritems():
        phoneme_chance_list[transition_phoneme] = num / num_occurrences
    phoneme_chain_prob[phoneme] = phoneme_chance_list
    '''
    total_prob = 0.0
    for transition_phoneme, chance in phoneme_chance_list.iteritems():
        total_prob += chance
    phoneme_chain_prob[phoneme]['TOTAL_PROB'] = total_prob
    '''

#print(phoneme_chain_absolute)
#print(phoneme_chain_prob)
print json.dumps(phoneme_chain_prob, indent=2)
