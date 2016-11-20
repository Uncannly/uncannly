import time, os, sys, random
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import file, format, present

most_probable_words = file.load('most_probable_words')

words = most_probable_words.keys()

print 'total generated most probable words: ', len(words)

while True:
	present.present(random.choice(words))