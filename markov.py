
def store_phoneme_transition_instance(first_phoneme, second_phoneme):
    print(first_phoneme + ' ' + second_phoneme)

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
