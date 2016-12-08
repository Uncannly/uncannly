# Uncann.ly

Get the most phonetically probable yet missing words of the English language.

Visit [http://uncannly.cfapps.io](http://uncannly.cfapps.io) for a demonstration.

## Endpoint versions:

### /random-word

Query params:

* `unweighted`: Do not weight probabilities by frequency of words in the corpus.
* `exclude-real`: Do not include words probable by pronunciation that do exist.

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

* `return-count`: How many words to return at once (default: `45`).
* `averaging`: Use the list of most likely words which was created by cutting off words when they passed a threshold based on averaging the probabilities of phonemes following each other (instead of taking the continued product of these probabilities, which is the default). 
* `random-selection`: From this particularly specified set of most probable words, instead of the absolute topmost probable ones, return a random selection.
* `unweighted`: Do not weight probabilities by frequency of words in the corpus.
* `exclude-real`: Do not include words probable by pronunciation that do exist.

e.g.

```
https://uncannly.cfapps.io/words?return-count=3&averaging&random-selection&unweighted&exclude-real
["s", "kʌntʌn", "kʌliʌn"]
```

```
https://uncannly.cfapps.io/words
["wɑz (WAAS)", "wɚ (WE'RE(2))", "ɪŋ (ING)", "wɑr", "ɪz (IS)", ...]
```

## Terminal script versions:

### bin/random_word

Arguments:

* `-u`, `--unweighted`: Do not weight probabilities by frequency of words in the corpus.
* `-x`, `--exclude-real`: Do not include words probable by pronunciation that do exist.

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

* `-c`, `--return-count`: How many words to return at once (default: `45`).
* `-a`, `--averaging`: Use the list of most likely words which was created by cutting off words when they passed a threshold based on averaging the probabilities of phonemes following each other (instead of taking the continued product of these probabilities, which is the default). 
* `-r`, `--random-selection`: From this particularly specified set of most probable words, instead of the absolute topmost probable ones, return a random selection.
* `-u`, `--unweighted`: Do not weight probabilities by frequency of words in the corpus.
* `-x`, `--exclude-real`: Do not include words probable by pronunciation that do exist.

e.g.

```
$ python bin/words.py -c 3 -a -r -u -x
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
