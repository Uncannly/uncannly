import time, os, sys, random
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import file, format, exists

most_probable_words = file.load('most_probable_words')

words = most_probable_words.keys()
print len(words)
while True:
	word = random.choice(words)
	existing_word = exists.already_in_dictionary(word)
	if existing_word:
		print '{} (word exists already: {})'.format(word, existing_word)
	else:
		print word
	time.sleep(0.2)