import time, os, sys, random
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import file, format, exists

most_probable_words = file.load('most_probable_words')

print len(most_probable_words)
sorted_most_probable_words = sorted(
	most_probable_words,
	key = most_probable_words.get,
	reverse = True
)
for word in sorted_most_probable_words:
	existing_word = exists.already_in_dictionary(word)
	if existing_word:
		print '{} (word exists already: {})'.format(word, existing_word)
	else:
		print word
	time.sleep(0.2)