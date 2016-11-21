import random, time, os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import random_probable_word

def get():
	random_probable_word.get(multiple=True)

# from lib import file, present, next_phoneme

# cumulative_distributions = file.load('cumulative_distributions')

# def get():
# 	phoneme = 'START_WORD'
# 	word = [phoneme]
# 	while True:
# 		phoneme = next_phoneme.next_phoneme(phoneme, random.random())
# 		if phoneme == 'END_WORD':
# 			present.present(word)
# 			phoneme = 'START_WORD'
# 			word = [phoneme]
# 		else:
# 			word.append(phoneme)

# get()