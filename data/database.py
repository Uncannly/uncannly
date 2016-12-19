import os, json, urlparse

import psycopg2
from cfenv import AppEnv

def connect():
	if os.environ.get('VCAP_SERVICES') is None:
		credentials = 'postgres://postgres:5554d58@localhost:5432/mydb'
	else:
		credentials = AppEnv().get_service(label='elephantsql').credentials['uri']

	parsed_credentials = urlparse.urlparse(credentials)
	return psycopg2.connect(
		database=parsed_credentials.path[1:],
		user=parsed_credentials.username,
		password=parsed_credentials.password,
		host=parsed_credentials.hostname
	)

def disconnect(connection):
	connection.commit()
	connection.close()

def do_the_words_table(words_for_db):
	connection = connect()

	sql_arr = []
	for words in words_for_db:
		sql_arr.append("('{}', '{}', '{}')".format(
			words[0].replace("'", "''"), 
			words[1].replace("'", "''"), 
			words[2].replace("'", "''")
		))

	cur = connection.cursor()
	sql = "insert into words (word, pronunciation, pronunciation_stressless) values"
	sql += ", ".join(sql_arr)
	cur.execute(sql)
	cur.close()

	disconnect(connection)

def do_a_phoneme_chain(phonemes, phonemes_unweighted, stressless):
	connection = connect()

	sql_arr = []
	for phoneme, sorted_list_of_next_phoneme_and_probability_tuples in phonemes.iteritems():
		sql_arr.append("('{}', '{}', '{}', '{}')".format(
			phoneme, 
			stressless, 
			json.dumps(sorted_list_of_next_phoneme_and_probability_tuples),
			json.dumps(phonemes_unweighted[phoneme]),
		))

	cur = connection.cursor()
	sql = "insert into phonemes (phoneme, stressless, next_phonemes, next_phonemes_unweighted) values"
	sql += ", ".join(sql_arr)
	cur.execute(sql)
	cur.close()
	disconnect(connection)

def load_words():
	connection = connect()

	cur = connection.cursor()
	sql = ";".join([
		"select * from words"
	])
	cur.execute(sql)
	results = cur.fetchall()
	cur.close()

	disconnect(connection)
	return results

def load_scores(stressless, unweighted, scoring_method):
	if scoring_method == 'integral_product':
		method_mean = False
		method_addition = False
	elif scoring_method == 'integral_sum':
		method_mean = False
		method_addition = True
	elif scoring_method == 'mean_geometric':
		method_mean = True
		method_addition = False
	elif scoring_method == 'mean_arithmetic':
		method_mean = True
		method_addition = True

	connection = connect()

	cur = connection.cursor()
	sql = ";".join([
		"select word, score from scores where \
			stressless = {} and unweighted = {} \
			and method_mean = {} and method_addition = {}".format(
				stressless, unweighted, method_mean, method_addition
			)
	])
	cur.execute(sql)
	results = cur.fetchall()
	cur.close()

	disconnect(connection)
	return results

def load_phonemes(stressless, unweighted):
	connection = connect()
	cur = connection.cursor()

	next_phonemes = 'next_phonemes_unweighted' if unweighted else 'next_phonemes'
	sql = ";".join([
		"select phoneme, {} from phonemes where stressless = {}".format(
			next_phonemes, stressless
		)
	])
	cur.execute(sql)
	results = cur.fetchall()
	cur.close()

	output = {}
	for phoneme, next_phonemes in results:
		output[phoneme] = json.loads(next_phonemes)

	disconnect(connection)
	return output