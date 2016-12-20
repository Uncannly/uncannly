import json

from database import execute

def schema(connection):
	sql_array = [
		"drop table if exists words",
		"create table words (word varchar, \
			pronunciation varchar, pronunciation_stress_ignored varchar)",
		"drop table if exists phonemes",
		"create table phonemes (phoneme varchar, stress_ignored boolean, \
			next_phonemes varchar, next_phonemes_unweighted varchar)",
		"drop table if exists scores",
		"create table scores (word varchar, score float(25), \
			stress_ignored boolean, unweighted boolean, \
			method_mean boolean, method_addition boolean)",
		""
	]
	sql_string = ";".join(sql_array)
	execute(connection, sql_string)

def words(connection, words_for_db):
	sql_array = []
	for words in words_for_db:
		sql_array.append("('{}', '{}', '{}')".format(
			words[0].replace("'", "''"), 
			words[1].replace("'", "''"), 
			words[2].replace("'", "''")
		))
	sql_string = "insert into words (word, pronunciation, pronunciation_stress_ignored) values"
	sql_string += ", ".join(sql_array)
	execute(connection, sql_string)

def phonemes(connection, phonemes, phonemes_unweighted, stress_ignored):
	sql_array = []
	for phoneme, sorted_list_of_next_phoneme_and_probability_tuples in phonemes.iteritems():
		sql_array.append("('{}', '{}', '{}', '{}')".format(
			phoneme, 
			stress_ignored, 
			json.dumps(sorted_list_of_next_phoneme_and_probability_tuples),
			json.dumps(phonemes_unweighted[phoneme]),
		))
	sql_string = "insert into phonemes (phoneme, stress_ignored, next_phonemes, next_phonemes_unweighted) values"
	sql_string += ", ".join(sql_array)
	execute(connection, sql_string)

def scores(connection, most_probable_words, stress_ignored, unweighted, method_mean, method_addition):
	sql_array = []
	for word, score in most_probable_words.iteritems():
		sql_array.append("('{}', '{}', '{}', '{}', '{}', '{}')".format(
			word, 
			score, 
			stress_ignored, 
			unweighted, 
			method_mean, 
			method_addition
		))
	sql_string = "insert into scores \
		(word, score, stress_ignored, unweighted, method_mean, method_addition) values"
	sql_string += ", ".join(sql_array)
	execute(connection, sql_string)
