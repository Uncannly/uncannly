import json

class Schema:
  def __init__(self, database):
    self.database = database

  def schema(self):
    sql_array = [
      "drop table if exists words",
      "create table words (word varchar, pronunciation varchar)",
      "drop table if exists phonemes",
      "create table phonemes (phoneme varchar, unstressed boolean, \
        next_phonemes varchar, next_phonemes_unweighted varchar)",
      "drop table if exists scores",
      "create table scores (word varchar, score real, \
        unstressed boolean, unweighted boolean, \
        method_mean boolean, method_addition boolean)",
      ""
    ]
    sql_string = ";".join(sql_array)
    self.database.execute(sql_string)

  def words(self, words):
    sql_array = []
    for word, pronunciation in words:
      sql_array.append("('{}', '{}')".format(
        word.replace("'", "''"), pronunciation
      ))
    sql_string = "insert into words (word, pronunciation) values"
    sql_string += ", ".join(sql_array)
    self.database.execute(sql_string)

  def phonemes(self, phonemes, next_phonemes_unweighted, unstressed):
    sql_array = []
    for phoneme, next_phonemes_for_this_phoneme in phonemes.iteritems():
      sql_array.append("('{}', '{}', '{}', '{}')".format(
        phoneme,
        unstressed,
        json.dumps(next_phonemes_for_this_phoneme),
        json.dumps(next_phonemes_unweighted[phoneme]),
      ))
    sql_string = (
      "insert into phonemes (phoneme, unstressed, "
        "next_phonemes, next_phonemes_unweighted) values"
    )
    sql_string += ", ".join(sql_array)
    self.database.execute(sql_string)

  def scores(self, most_probable_words, options):
    sql_array = []
    for word, score in most_probable_words:
      sql_array.append(
        "('{}', '{}', '{}', '{}', '{}', '{}')".format(word, score, *options)
      )
    sql_string = (
      "insert into scores "
      "(word, score, unstressed, unweighted, method_mean, method_addition)"
      "values"
    )
    sql_string += ", ".join(sql_array)
    self.database.execute(sql_string)

  def finish(self):
    self.database.disconnect()