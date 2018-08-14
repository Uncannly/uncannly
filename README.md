# Uncann.ly

Get the most phonetically probable yet missing words of the English language.

Visit [http://uncannly.douglasblumeyer.com](http://uncannly.douglasblumeyer.com) for a demonstration.

We can choose from two **modes** of finding these words:

1) In **random** mode, we generate words from scratch on the fly, each time using a [Markov chain](https://en.wikipedia.org/wiki/Markov_chain) of phonemes.
2) In **top** mode, we draw from a pre-generated list of the very most likely words possible to be generated by this same chain.

Both of these modes are available in three interfaces:

### web

http://uncannly.douglasblumeyer.com

### API

https://uncannly.douglasblumeyer.com/random

https://uncannly.douglasblumeyer.com/top

### CLI

```
$ chiry@munscalune:~/workspace/uncannly: python bin/random_mode.py
M AH1 N S T AH0 N
AHO V ER1 D ER0
P AH1 T (PUTT)
...

$ chiry@munscalune:~/workspace/uncannly: python bin/top_mode.py
W AA1 Z (WAAS)
W ER0 (WERE)
S T
W AA1 R
...
```

Words are currently limited to 20 letters regardless of any options.

Uncannly has some pretty reasonable defaults, but also plenty of options to tailor to your needs. All of the following are available both as parameters on the API and as flags on the CLI.

## Options

<a name="pool">
### pool
</a>

How many words to gather by the chosen mode. *Default: 45.*

CLI shortcut: `-p`

### selection

When enabled, use the other mode to select words from the [**pool**](#pool).

For example, in **top** mode, this option causes words to be randomly selected from the top pool. 

* When enabled but no value is provided, the effect is to scramble the words from their exact ranking, and probably to miss out on seeing some altogether due to random repeated selection of ones already in the returned list.
* After adding value to lock down a return count, increase the [**pool**](#pool) to increase the proportion of less probable words (because the words will be being randomly drawn from a pool which extends deeper into the realm of less probable words).

Conversely, in **random** mode, take the same action to cause the opposite effect: decrease the proportion of more probable words within the locked-down selection count. 

* This happens because more and more random words are generated, and with each new one there is a chance it might be more probable than ones already generated, thus displacing the least probable of those slated to be returned.
* In random mode, enabling **selection** without adding a value just has the effect of sorting your random words.

The selection can be larger than the [**pool**](#pool), though there's not much point. In fact there is no effect at all when in **top** mode, and when in **random** mode it just increases the repetition in the returned words of the words from the pool (and the chances that each of those words get returned at all). Given how unuseful this situation is, the web interface prevents it (but it is still possible using either the API or the CLI).

`top-selection` (CLI shortcut `-t`) aliases `selection` when in random mode.

`random-selection` (CLI shortcut `-w`) aliases `selection` when in top mode.

*Default: disabled (when enabled, defaults to 10).*

CLI shortcut: `-s`

<a name="scoring-method">
### scoring method
</a>

The method used to score words by, for ranking them and filtering out the lower scoring ones. 

Four scoring methods exist in a 2×2 matrix relationship:

| operation \ value | total               | average           |
| ----------------- | ------------------ | ----------------- |
| **multiplication**    | **integral product** | **mean geometric**   |
| **addition**          | **integral sum**     | **mean arithmetic** |

1) **integral product**: the probability from each phoneme to the next is continuously multiplied.
2) **integral sum**: the probability from each phoneme to the next is continuously added (except that it's actually 1 minus each probability which gets summed, and then the reciprocal of that number so that we can sort the same direction as the other three methods). 
3) **mean geometric**: like the integral product except that the nth root of the result is taken, where n is the number of phonemes up to that point.
4) **mean arithmetic**: just the average of all probabilies thus far.

The **total** methods give a measure of "out of all the possible words, what is the actual chance of this word". Since the probability of a given next phoneme is never greater than 1, adding a new phoneme can only decrease the score. Therefore totalling methods are biased toward shorter words. 

The **average** methods do allow for new phonemes to actually increase the score of a word. For example, the word "jyɑtɚdʌnd" gets off to a really rough start, but the rest of the word consists of very common phoneme transitions. Average methods allow for weirder phoneme transitions to occur up front without nixing the pathway to generating words, and allow for longer words.

Filtering will not occur unless a [**score threshold**](#score-threshold) is specified as well; only ranking will occur.

Scoring is required when filtering (one must filter by something). Filtering is optional for the **random** mode, but it is required for this most probable **top** mode, because the possibility space is too large to traverse without some filter.

*Default: integral product.*

CLI shortcut: `-sm`

`-ip` aliases `-sm integral-product`.

`-is` aliases `-sm integral-sum`.

`-mg` aliases `-sm mean-geometric`.

`-ma` aliases `-sm mean-arithmetic`.


<a name="score-threshold">
### score threshold
</a>

When specified, will not return words with scores lower than this threshold (according to the current [**scoring method**](#scoring-method)).

*Default: 1^10-7, which is the threshold which still lets 45 words through for the default scoring method, integral product. All other scoring methods need higher thresholds to filter out more words than that.*

CLI shortcut: `-st`

### unweighted

Do not weight probabilities by frequency of words in the corpus.

CLI shortcut: `-xw`

### unstressed

Ignore stress levels of vowels.

CLI shortcut: `-xs`

### exclude real

Do not include words probable by pronunciation that do exist.

CLI shortcut: `-xr`

### ignore position

Do not consider phoneme or syllable position within the word when choosing the next one.

CLI shortcut: `-xp`

### ignore length

Do not consider length of the word in phonemes or syllables when choosing the next one. I will say more on this later.

CLI shortcut: `-xl`

### maximum length

The maximum length (in phonemes or syllables) of words to return.

CLI shortcut: `-mx`

### minimum length

The minimum length (in phonemes or syllables) of words to return.

CLI shortcut: `-mn`

### ignore syllables

Use phonemes instead of syllables as the unit of sound to generate words by. This will result in less natural words, as Uncannly will not understand stress patterns. It will also not be drawing from preestablished consonant clusters. However it will tend to give more original words. 

CLI shortcut: `-xy`

## Examples

https://uncannly.douglasblumeyer.com/random

```
$ chiry@munscalune:~/workspace/uncannly: python bin/random_mode.py
M AH0 P R IY0 W ER0
DH EH1 R (THEIR)
R IH0 S AH1 M B IY1 ZH AH0 L AY1 L IY0 TH AW1
AE1 S IY1 D IH0 SH IH0 T R D
...
```

https://uncannly.douglasblumeyer.com/random?pool=5&selection=3&scoring-method=mean-geometric&score-threshold=0.0000000000001&unweighted&unstressed&exclude-real

```
$ chiry@munscalune:~/workspace/uncannly: python bin/random_mode.py -p 5 -s 3 -mg -st 0.0000000000001 -xw -xs -xr -xp -xl
S IH NG G ER
S T AY P ER
K AA R EY D AY T S AH L AH S
```

https://uncannly.douglasblumeyer.com/top

```
$ chiry@munscalune:~/workspace/uncannly: python bin/top_mode.py
W AA1 Z (WAAS)
W ER0 (WERE)
S T
W AA1 R
...
```

https://uncannly.douglasblumeyer.com/top?pool=500&selection=3&scoring-method=integral-sum&score-threshold=0.01&unweighted&unstressed&exclude-real
```
$ chiry@munscalune:~/workspace/uncannly: python bin/top_mode.py -p 500 -s 3 -is -st 0.1 -xw -xs -xr -xp -xl
K AA N T
M AH
B ER Z AH N
```



## Development

### 1. Install python

Use an installer to get 2.7.12 on your system.
Add `C:\Python27` to your path in System Environment Variables.

### 2. Install pip

Download get-pip and run it with your newfound python.
Add `C:\Python27\Scripts` to your path in System Environment Variables.

### 3. Install virtualenv and pylint globally

```
$ chiry@munscalune:~/workspace: pip install virtualenv pylint
```

### 4. Fork and clone repo

```
$ chiry@munscalune:~/workspace: git clone your-fork.git
$ chiry@munscalune:~/workspace: cd uncannly
```

### 5. Configure python path

Both permanently and for this session.

```
$ chiry@munscalune:~/workspace: echo 'export PYTHONPATH=$PYTHONPATH:~/workspace/uncannly' >> ~/.bash_profile
$ chiry@munscalune:~/workspace: . ~/.bash_profile
```

### 6. Install project dependencies

```
$ chiry@munscalune:~/workspace/uncannly: virtualenv venv
$ chiry@munscalune:~/workspace/uncannly: source venv/bin/activate
$ chiry@munscalune:~/workspace/uncannly: pip install -r requirements.txt
```

Note that on Windows this may be `venv/Scripts/activate` instead.

### 7. Install postgres

Set your local database credentials to `postgres:duperuser`.
Create a database called `uncannly`.
Start on the default 5432 port.

### 8. Set up database

```
$ chiry@munscalune:~/workspace/uncannly: python bin/initialize_database.py
Database successfully initialized.
```

### 9. Start up app

```
$ chiry@munscalune:~/workspace/uncannly: python app/app.py
```

On Windows `python -m app.app` may work instead. Something to do with the way modules find each other differently.

Now you can visit a local version of the app at `localhost:5000`.

### 10. Develop

You may want to mark `/venv`, `/data/primary_data`, and `data/secondary_data` as excluded in your IDE to retain sane search results.

### 11. Linting & Testing

Neither currently passing, but they're supposed to be `pylint uncannly > pylint.log` and `nosetests` respectively.

### 12. Deploy

You'll need to create the file `production_database_credentials.txt` in the root with the full URL for your production database (the one including the hostname, database name, username, and password).

```
python -m bin.initialize_database --production
cf push
``` 

## Development w/r/t GCP

For it to work on GCP I had to follow these instructions:
https://cloud.google.com/appengine/docs/flexible/python/using-cloud-sql-postgres#setting_up_your_local_environment

First I created the project for Uncannly on GCP.

Then I enabled the "Cloud SQL Admin API" for the project.

Then I downloaded, installed, and initialized the `gcloud` CLI (AKA the "Cloud SDK").

Locally, I created a `gcloud` configuration:

```
gcloud config configurations create uncannly
gcloud config set project uncannly
gcloud config set account kingwoodchuckii@gmail.com
```

Then I created a "Cloud SQL for PostgreSQL instance" following these instructions:
https://cloud.google.com/sql/docs/postgres/create-instance

```
gcloud sql instances create [INSTANCE_NAME] --database-version=POSTGRES_9_6 --cpu=1 --memory=3840MiB
gcloud sql users set-password [USER] no-host --instance [INSTANCE_NAME] --password [PASSWORD]
gcloud sql databases create [DATABASE_NAME] --instance [INSTANCE_NAME]
gcloud sql instances describe [INSTANCE_NAME]
```
In the output from the last command you can get the `connectionName` which is thenceforth `[CONNECTION_NAME]`, which you need for later steps.

In order to seed the database, you'll need to use the proxy Google provides:

```
gcloud auth application-default login
curl -o cloud_sql_proxy https://dl.google.com/cloudsql/cloud_sql_proxy.darwin.amd64
chmod +x cloud_sql_proxy
./cloud_sql_proxy -instances=[CONNECTION_NAME]=tcp:5432
```

Regarding the Postgres connection string in `database.py`:
For now, I am not going to bother myself with getting the connection string/URL correct / automating environment detection etc. w/r/t GCP.
For now, if you need to seed the database from local, manually replace these lines temporarily:

```
    return psycopg2.connect(
        database = [DATABASE_NAME],
        user = [USER],
        password = [PASSWORD],
        host = "localhost"
    )
```

then run the normal `python bin/initialize_database.py` script.

And if you need to deploy to GCP, manually replace these lines temporarily:
```
    return psycopg2.connect(
        database = [DATABASE_NAME],
        user = [USER],
        password = [PASSWORD],
        host = "/cloudsql/[CONNECTION_NAME]"
    )
```
then (assuming you've activated the configuration for `uncannly`) just run `gcloud app deploy`.
