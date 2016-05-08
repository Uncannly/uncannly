phoneme_chain = {}

def store_phoneme_transition_instance(first_phoneme, second_phoneme):
    if first_phoneme not in phoneme_chain:
        phoneme_chain[first_phoneme] = {}
    if second_phoneme not in phoneme_chain[first_phoneme]:
        phoneme_chain[first_phoneme][second_phoneme] = 1
    else:
        phoneme_chain[first_phoneme][second_phoneme] += 1

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

print(phoneme_chain)
