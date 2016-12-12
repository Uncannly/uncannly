# Uncann.ly

Get the most phonetically probable yet missing words of the English language.

Visit [http://uncannly.cfapps.io](http://uncannly.cfapps.io) for a demonstration.

## Options

* **return count**

How many words to return at once (default: 45).

* **scoring method**

The method used to score words by, and filter out the lower scoring ones. Four methods exist in a 2×2 matrix relationship:

| operation \ value | total              | average           |
| ----------------- | ------------------ | ----------------- |
| multiplication    | `integral-product` | `mean-geometric`  |
| addition          | `integral-sum`     | `mean-arithmetic` |

1) `integral-product`: the probability from each phoneme to the next is continuously multiplied.
2) `integral-sum`: the probability from each phoneme to the next is continuously added (except that it's actually 1 minus each probability which gets summed, and then the reciprocal of that number so that we can sort the same direction as the other three methods). 
3) `mean-geometric`: like the integral product except that the nth root of the result is taken, where n is the number of phonemes up to that point.
4) `mean-arithmetic`: just the average of all probabilies thus far.

The "total" methods give a measure of "out of all the possible words, what is the actual chance of this word". Since the probability of a given next phoneme is never greater than 1, adding a new phoneme can only decrease the score. Therefore totalling methods are biased toward shorter words. 

The "average" methods do allow for new phonemes to actually increase the score of a word. For example, the word "jyɑtɚdʌnd" gets off to a really rough start, but the rest of the word consists of very common phoneme transitions. Average methods allow for weirder phoneme transitions to occur up front without nixing the pathway to generating words, and allow for longer words.

Scoring is required when filtering (one must filter by something). Filtering is optional for the `random-word` mode, but it is required for this most probable `words` mode, because the possibility space is too large to traverse without some filter. Therefore, scoring is required for `words` mode. 

The default scoring method is `integral-product`.

* **score threshold**

When specified, will not return words with scores (according to the current scoring method) lower than this threshold.

* **random selection**

Return a random set of words drawn from a pool at the top, rather than a ranked list from the top.

If you pass a value, it will be taken as the number of words to include in the pool. 

The value may be lower than the return count. You will just get more repeats than you might normally.

The maximum and default are both 1000000.

* **unweighted**

Do not weight probabilities by frequency of words in the corpus.

* **exclude real**

Do not include words probable by pronunciation that do exist.

## Endpoint versions:

### /random-word

Query params:
* `unweighted`
* `exclude-real`

e.g.

```
https://uncannly.cfapps.io/random-word?unweighted&exclude-real
"fɑɪtrɛθrikɑtɪvʌltʌn"
```

```
https://uncannly.cfapps.io/random-word
"pɑtɛndemɛðɛθ"
```

### /words

Query params:
* `return-count`
* `scoring-method`
* `score-by-integral-product`
* `score-by-integral-sum`
* `score-by-mean-geometric`
* `score-by-mean-arithmetic`
* `random-selection`
* `unweighted`
* `exclude-real`

e.g.

```
https://uncannly.cfapps.io/words?return-count=3&scoring-method=mean-arithmetic&random-selection=500&unweighted&exclude-real
["s", "kʌntʌn", "kʌliʌn"]
```

```
https://uncannly.cfapps.io/words
["wɑz (WAAS)", "wɚ (WE'RE(2))", "ɪŋ (ING)", "wɑr", "ɪz (IS)", ...]
```

## Terminal script versions:

### bin/random_word

Arguments:
* `-u`, `--unweighted`
* `-x`, `--exclude-real`

e.g.

```
$ python bin/random_word.py -u -x
Y UW Z IH T AH Z
```

```
$ python bin/random_word.py
G EH R (GAIR)
```

### bin/words

Arguments:
* `-c`, `--return-count`
* `-m`, `--scoring-method`
* `-p`, `--score-by-integral-product`
* `-s`, `--score-by-integral-sum`
* `-g`, `--score-by-mean-geometric`
* `-a`, `--score-by-mean-arithmetic`
* `-r`, `--random-selection`
* `-u`, `--unweighted`
* `-x`, `--exclude-real`

e.g.

```
$ python bin/words.py -c 3 -a -r 500 -u -x
K AH L IY AH N
K AH N T AH N
S
```

```
$ python bin/words.py
W AA Z (WAAS)
W ER (WE'RE(2))
IH NG (ING)
W AA R
IH Z (IS)
...
```