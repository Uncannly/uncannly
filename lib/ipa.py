# -*- coding: utf-8 -*-

def is_vowel(phoneme):
    return phoneme in IPA['vowels'].keys()

def ipa(word):
    output = []
    for phoneme in word:
        ipa = IPA['vowels'].get(phoneme)
        if ipa is None:
            ipa = IPA['consonants'].get(phoneme)
        output.append(ipa)
    return ''.join(output)

def destress(word):
    for character in "012":
        if character in word:
            word = word.replace(character, '')
    return word

IPA = {
    'vowels': {
        'AA': 'ɑ',  'AA1': 'ɑː',  'AA2': 'ɑ',  'AA0': 'ə',
        'AE': 'æ',  'AE1': 'æ',   'AE2': 'æ',  'AE0': 'ə',
        'AH': 'ʌ',  'AH1': 'ʌ',   'AH2': 'ʌ',  'AH0': 'ə',
        'AO': 'ɔ',  'AO1': 'ɔː',  'AO2': 'ɔ',  'AO0': 'ə',
        'AW': 'aʊ', 'AW1': 'aʊ',  'AW2': 'aʊ', 'AW0': 'ə',
        'AY': 'aɪ', 'AY1': 'aɪ',  'AY2': 'aɪ', 'AY0': 'ɨ',
        'EH': 'ɛ',  'EH1': 'ɛ',   'EH2': 'ɛ',  'EH0': 'ɨ',
        'ER': 'ɚ',  'ER1': 'ɜːr', 'ER2': 'ɚ',  'ER0': 'ɚ',
        'EY': 'eɪ', 'EY1': 'eɪ',  'EY2': 'eɪ', 'EY0': 'ɨ',
        'IH': 'ɪ',  'IH1': 'ɪ',   'IH2': 'ɪ',  'IH0': 'ɨ',
        'IY': 'i',  'IY1': 'iː',  'IY2': 'i',  'IY0': 'ɨ',
        'OW': 'o',  'OW1': 'oʊ',  'OW2': 'o',  'OW0': 'ə',
        'OY': 'ɔɪ', 'OY1': 'ɔɪ',  'OY2': 'ɔɪ', 'OY0': 'ɔɪ',
        'UH': 'ʊ',  'UH1': 'ʊ',   'UH2': 'ʊ',  'UH0': 'ᵿ',
        'UW': 'uː', 'UW1': 'uː',  'UW2': 'uː', 'UW0': 'u'
    },
    'consonants': {
        'B':  'b',
        'CH': 't͡ʃ',
        'D':  'd',
        'DH': 'ð',
        'F':  'f',
        'G':  'g',
        'HH': 'h',
        'JH': 'd͡ʒ',
        'K':  'k',
        'L':  'l',
        'M':  'm',
        'N':  'n',
        'NG': 'ŋ', 
        'P':  'p',
        'R':  'r',
        'S':  's',
        'SH': 'ʃ',
        'T':  't',
        'TH': 'θ',
        'V':  'v',
        'W':  'w',
        'Y':  'j',
        'Z':  'z',
        'ZH': 'ʒ'
    }
}
