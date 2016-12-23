from open_helper import open_primary_data_file

def parse():
	word_frequencies = {}

	file = open_primary_data_file('unlemmatized_frequency_list')
	for line in file:
		line_split_by_spaces = line.strip().split(' ')
		frequency = line_split_by_spaces[0]
		word = line_split_by_spaces[1].upper()
		word_frequencies[word] = int(frequency)
	file.close()

	return word_frequencies