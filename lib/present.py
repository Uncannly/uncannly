import sys

from lib.ipa import ipa, destress, stress_level, stress_symbol
from lib.conversion import array_to_string, to_sig_figs
from data.load_data import load_words

WORDS = load_words()

def for_web(word, score, unstressed, exclude_real):
    ipa_word = ipa(word)

    stringified_word = array_to_string(word)
    existing_word = _already_in_dictionary(stringified_word, unstressed)

    return _present_word(ipa_word, score, exclude_real, existing_word)

# pylint: disable=too-many-arguments
def for_terminal(word, score, unstressed, exclude_real, ignore_syllables, suppress_immediate):
    if not ignore_syllables:
        word = ' '.join([' '.join(syllable) for syllable in word])
    existing_word = _already_in_dictionary(word, unstressed)
    word, score = _present_word(word, score, exclude_real, existing_word)
    if not word:
        return False
    else:
        if not suppress_immediate:
            sys.stdout.write(word + ' [' + str(to_sig_figs(score, 6)) + ']\n')
        return word, score
# pylint: enable=too-many-arguments

def for_web_syllables(word, score, unstressed, exclude_real):
    if word == []:
        return None
    word_output = ''
    for_checking_word = []
    for syllable in word:
        stress = stress_level(syllable)
        if stress == 'primary' or stress == 'secondary':
            word_output += stress_symbol(stress)

        for phoneme in syllable:
            word_output += ipa([phoneme])
            for_checking_word.append(phoneme)
    existing_word = _already_in_dictionary(' '.join(for_checking_word), unstressed)
    return _present_word(word_output, score, exclude_real, existing_word)

def for_terminal_selection(words):
    for word, score in words:
        sys.stdout.write(word + ' [' + str(to_sig_figs(score, 6)) + ']\n')

def _present_word(word, score, exclude_real, existing_word):
    score = to_sig_figs(score, 6)
    if existing_word:
        return False if exclude_real else ('{} ({})'.format(word, existing_word), score)
    else:
        return word, score

def _already_in_dictionary(word, unstressed):
    highest_frequency = 0
    best_match = None
    for spelling, pronunciation, frequency in WORDS:
        if unstressed:
            pronunciation = destress(pronunciation)

        if word == pronunciation and frequency > highest_frequency:
            best_match = spelling
            highest_frequency = frequency

    return best_match
