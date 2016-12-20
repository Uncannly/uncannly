import os

def parse():
	word_frequencies = {}

	pwd = os.path.dirname(__file__)
	file = open(os.path.join(pwd, '..', '..', '..', 'data', 'primary_data', 'unlemmatized_frequency_list.txt'), 'r')
	for line in file:
		line_split_by_spaces = line.strip().split(' ')
		frequency = line_split_by_spaces[0]
		word = line_split_by_spaces[1].upper()
		word_frequencies[word] = int(frequency)
	file.close()
	
	return word_frequencies