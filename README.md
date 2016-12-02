# Uncann.ly

Get the most phonetically probable yet missing words in the English language.

Visit [http://uncannly.cfapps.io](http://uncannly.cfapps.io) for a demonstration.

## Endpoints:

/random_word
Query params:
* weighted_by_frequency: true/false
* include_real_words: true/false

/words
Query params:
* selection: top, random
* threshold: continued_product, averaging
* weighted_by_frequency: true/false
* include_real_words: true/false
* return_count: int < several thousand or so I guess

i.e.
words?selection=top&threshold=continued_product&weighted_by_frequency=true&include_real_words=true&return_count=4

## Terminal scripts:

bin/random_word

bin/words
Flags:
* -u --unweighted 
* -x --exclude-real-words
* -a --by-averaging            
* -c --by-continued-product   
* -r --random (default is top)