import file, format, present

def share(style):
	most_probable_words = file.load('most_probable_words_by_{}'.format(style))

	print 'total generated most probable words:', len(most_probable_words)

	sorted_most_probable_words = sorted(
		most_probable_words,
		key = most_probable_words.get,
		reverse = True
	)

	for word in sorted_most_probable_words:
		present.present(word)