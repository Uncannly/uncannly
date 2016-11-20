def parse():
	word_freqs = {}

	f = open('primary_data/unlemmatized_frequency_list.txt', 'r')
	for line in f:
			split_by_tabs = line.strip().split(' ')
			freq = split_by_tabs[0]
			word = split_by_tabs[1].upper()
			word_freqs[word] = freq
	f.close()
	
	return word_freqs