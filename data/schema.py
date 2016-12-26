import json

class Schema(object):
    def __init__(self, database):
        self.database = database

    def schema(self):
        sql_array = [
            "drop table if exists words",
            "create table words (word varchar, pronunciation varchar)",
            "drop table if exists phonemes",
            "create table phonemes (word_position int, phoneme varchar, \
              unstressed boolean, next_phonemes varchar, \
              next_phonemes_unweighted varchar)",
            "drop table if exists scores",
            "create table scores (word varchar, score real, \
              ignore_position boolean, unstressed boolean, unweighted boolean, \
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
        sql_string = "insert into words (word, pronunciation) values "
        sql_string += ", ".join(sql_array)
        self.database.execute(sql_string)

    def phonemes(self, word_positions, word_positions_unweighted, unstressed):
        sql_array = []
        for i in range(0, len(word_positions)):
            # print word_positions[i]
            # raw_input()
            for phoneme, next_phonemes in word_positions[i].iteritems(): 
                next_phonemes_unweighted = word_positions_unweighted[i][phoneme]
                sql_array.append("('{}', '{}', '{}', '{}', '{}')".format(
                    i,
                    phoneme,
                    unstressed,
                    json.dumps(next_phonemes),
                    json.dumps(next_phonemes_unweighted)
                ))
        sql_string = (
            "insert into phonemes (word_position, phoneme, unstressed, "
            "next_phonemes, next_phonemes_unweighted) values "
        )
        sql_string += ", ".join(sql_array)
        self.database.execute(sql_string)

    def scores(self, most_probable_words, options):
        if len(most_probable_words) == 0:
            return
        else:
            sql_array = []
            for word, score in most_probable_words:
                sql_array.append(
                    "('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(word, score, *options)
                )
            sql_string = (
                "insert into scores "
                "(word, score, ignore_position, unstressed, unweighted, method_mean, method_addition) "
                "values "
            )
            sql_string += ", ".join(sql_array)
            self.database.execute(sql_string)

    def finish(self):
        self.database.disconnect()
