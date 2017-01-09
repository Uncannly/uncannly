import sys

from lib.ipa import ipa, destress, stress_level, stress_symbol
from lib.conversion import array_to_string
from data.load_data import load_words

WORDS = load_words()

def for_web(word_and_score, unstressed, exclude_real):
    word, score = word_and_score
    ipa_word = ipa(word)

    stringified_word = array_to_string(word)
    existing_word = _already_in_dictionary(stringified_word, unstressed)

    return _present_word(ipa_word, score, exclude_real, existing_word)

def for_terminal(word_and_score, unstressed, exclude_real, suppress_immediate):
    word, score = word_and_score
    existing_word = _already_in_dictionary(word, unstressed)
    word_and_score = _present_word(word, score, exclude_real, existing_word)
    if not word:
        return False
    else:
        if not suppress_immediate:
            sys.stdout.write(word + ' [' + str(score) + ']\n')
        return word_and_score

def for_web_syllables(word, exclude_real):
    if word == []:
        return None
    word_output = ''
    for_checking_word = []
    for syllable in word:
        stress = stress_level(syllable)
        if stress == 'primary' or stress == 'secondary':
            word_output += stress_symbol(stress)

        for phoneme in syllable:
            if phoneme != 'END_WORD':
                word_output += ipa([phoneme])
                for_checking_word.append(phoneme)
    existing_word = _already_in_dictionary(' '.join(for_checking_word), False)
    if existing_word:
        if exclude_real:
            return None
        else:
            word_output += ' (' + existing_word + ')'
    return word_output

def _present_word(word, score, exclude_real, existing_word):
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
