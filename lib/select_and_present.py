from sys import stdout

from lib.ipa import ipa, destress, stress_level, stress_symbol
from lib.conversion import data_to_formatted_string, to_sig_figs
from data.load_data import load_words

WORDS = load_words()

def select_for_web(word, score, unstressed, exclude_real, ignore_syllables, _=None):
    web_helper = _web_phonemes if ignore_syllables else _web_syllables
    output, check = web_helper(word)

    existing_word = _already_in_dictionary(check, unstressed)
    return _format_or_reject(output, score, exclude_real, existing_word)

# pylint: disable=too-many-arguments,invalid-name
def select_and_maybe_present_for_terminal(word, score, unstressed, exclude_real,\
    ignore_syllables, suppress_immediate_presentation):
    word = data_to_formatted_string(word, ignore_syllables)
    existing_word = _already_in_dictionary(word, unstressed)
    word_and_score = _format_or_reject(word, score, exclude_real, existing_word)
    if word_and_score is None:
        return None
    else:
        word, score = word_and_score
        if not suppress_immediate_presentation:
            _write_to_terminal(word, score)
        return word, score
# pylint: enable=too-many-arguments,invalid-name

def terminal_delayed_presentation(words):
    for word, score in words:
        _write_to_terminal(word, score)
    return True

def terminal_failure(message):
    stdout.write(message + '\n')
    return True

def _web_phonemes(word):
    return ipa(word), data_to_formatted_string(word, ignore_syllables=True)

def _web_syllables(word):
    word_output = ''
    for_checking_word = []
    for syllable in word:
        stress = stress_level(syllable)
        if stress == 'primary' or stress == 'secondary':
            word_output += stress_symbol(stress)

        for phoneme in syllable:
            word_output += ipa([phoneme])
            for_checking_word.append(phoneme)
    # yes, it is weird that we claim to ignore syllables though we're in syllables
    return word_output, data_to_formatted_string(for_checking_word, ignore_syllables=True)

def _write_to_terminal(word, score):
    stdout.write(word + ' [' + str(to_sig_figs(score, 6)) + ']\n')

def _format_or_reject(word, score, exclude_real, existing_word):
    score = to_sig_figs(score, 6)
    if existing_word:
        return None if exclude_real else ('{} ({})'.format(word, existing_word), score)
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
