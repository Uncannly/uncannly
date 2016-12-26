# -*- coding: utf-8 -*-

def ipa(word):
    output = []
    for phoneme in word:
        output.append(IPA[phoneme])
    return ''.join(output)

def destress(word):
    for character in "012":
        if character in word:
            word = word.replace(character, '')
    return word

IPA = {
    'AA': 'ɑ',  'AA1': 'ɑː',  'AA2': 'ɑ',  'AA0': 'ə',
    'AE': 'æ',  'AE1': 'æ',   'AE2': 'æ',  'AE0': 'ə',
    'AH': 'ʌ',  'AH1': 'ʌ',   'AH2': 'ʌ',  'AH0': 'ə',
    'AO': 'ɔ',  'AO1': 'ɔː',  'AO2': 'ɔ',  'AO0': 'ə',
    'AW': 'ɑʊ', 'AW1': 'ɑʊ',  'AW2': 'ɑʊ', 'AW0': 'ə',
    'AY': 'ɑɪ', 'AY1': 'ɑɪ',  'AY2': 'ɑɪ', 'AY0': 'ɨ',
    'B':  'b',
    'CH': 'tʃ',
    'D':  'd',
    'DH': 'ð',
    'EH': 'ɛ',  'EH1': 'ɛ',   'EH2': 'ɛ',  'EH0': 'ɨ',
    'ER': 'ɚ',  'ER1': 'ɜːr', 'ER2': 'ɚ',  'ER0': 'ɚ',
    'EY': 'e',  'EY1': 'eɪ',  'EY2': 'e',  'EY0': 'ɨ',
    'F':  'f',
    'G':  'g',
    'HH': 'h',
    'IH': 'ɪ',  'IH1': 'ɪ',   'IH2': 'ɪ',  'IH0': 'ɨ',
    'IY': 'i',  'IY1': 'iː',  'IY2': 'i',  'IY0': 'ɨ',
    'JH': 'dʒ',
    'K':  'k',
    'L':  'l',
    'M':  'm',
    'N':  'n',
    'NG': 'ŋ',
    'OW': 'o',  'OW1': 'oʊ',  'OW2': 'o',  'OW0': 'ə',
    'OY': 'ɔɪ', 'OY1': 'ɔɪ',  'OY2': 'ɔɪ', 'OY0': 'ɔɪ',
    'P':  'p',
    'R':  'r',
    'S':  's',
    'SH': 'ʃ',
    'T':  't',
    'TH': 'θ',
    'UH': 'ʊ',  'UH1': 'ʊ',   'UH2': 'ʊ',  'UH0': 'ᵿ',
    'UW': 'uː', 'UW1': 'uː',  'UW2': 'uː', 'UW0': 'u',
    'V':  'v',
    'W':  'w',
    'Y':  'j',
    'Z':  'z',
    'ZH': 'ʒ'
}
