def parse():
	word_frequencies = {}

	file = open('data/primary_data/unlemmatized_frequency_list.txt', 'r')
	for line in file:
		line_split_by_tabs = line.strip().split(' ')
		frequency = line_split_by_tabs[0]
		word = line_split_by_tabs[1].upper()
		word_frequencies[word] = int(frequency)
	file.close()
	
	return word_frequencies