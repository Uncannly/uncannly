# -*- coding: utf-8 -*-

def ipa(word):
	output = []
	for phoneme in word:
		output.append(ipa_map[phoneme])
	return ''.join(output)

ipa_map = {
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