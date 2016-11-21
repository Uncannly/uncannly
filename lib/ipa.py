# -*- coding: utf-8 -*-

ipa_dict = {
	'AA':	'ɑ',
	'AE':	'æ',
	'AH':	'ʌ',
	'AO':	'ɔ',
	'AW':	'ɑʊ',
	'AY':	'ɑɪ',
	'B':	'b',
	'CH':	'tʃ',
	'D':	'd',
	'DH':	'ð',
	'EH':	'ɛ',
	'ER':	'ɚ',
	'EY':	'e',
	'F':	'f',
	'G':	'g',
	'HH':	'h',
	'IH':	'ɪ',
	'IY':	'i',
	'JH':	'dʒ',
	'K':	'k',
	'L':	'l',
	'M':	'm',
	'N':	'n',
	'NG':	'ŋ',
	'OW':	'o',
	'OY':	'ɔɪ',
	'P':	'p',
	'R':	'r',
	'S':	's',
	'SH':	'ʃ',
	'T':	't',
	'TH':	'θ',
	'UH':	'ʊ',
	'UW':	'u',
	'V':	'v',
	'W':	'w',
	'Y':	'y',
	'Z':	'z',
	'ZH':	'ʒ'
}

def ipa_map(phoneme):
	return ipa_dict[phoneme]

def ipa(word):
	return ''.join(map(ipa_map, word))