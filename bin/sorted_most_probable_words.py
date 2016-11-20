import time, os, sys, random
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from lib import file, format, present

most_probable_words = file.load('most_probable_words')

print 'total generated most probable words: ', len(most_probable_words)

sorted_most_probable_words = sorted(
	most_probable_words,
	key = most_probable_words.get,
	reverse = True
)

for word in sorted_most_probable_words:
	present.present(word)