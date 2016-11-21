# Most Phonetically Probable Missing English Words

Visit [http://most-phonetically-probable-missing-english-words.cfapps.io](http://most-phonetically-probable-missing-english-words.cfapps.io) for a demonstration.

## Endpoints:

/random_word

/words
Query params:
* style: sorted, random
* filter: continued_product, averaging
* weighted_by_frequency: true/false
* include_real_words: true/false
* return_count: int < several thousand or so I guess

i.e.
words?style=sorted&filter=continued_product&weighted_by_frequency=true&include_real_words=true&return_count=4