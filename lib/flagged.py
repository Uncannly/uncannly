import sys

def flagged(single_char_flag, full_word_flag):
	return single_char_flag in sys.argv or full_word_flag in sys.argv