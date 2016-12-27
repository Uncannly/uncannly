import json

class Schema(object):
    def __init__(self, database):
        self.database = database

    def schema(self):
        sql_array = [
            "drop table if exists words",
            "create table words (word varchar, pronunciation varchar)",
            "drop table if exists phonemes",
            "create table phonemes (word_length int, word_position int, \
              phoneme varchar, unstressed boolean, next_phonemes varchar, \
              next_phonemes_unweighted varchar)",
            "drop table if exists scores",
            "create table scores (word varchar, score real, length int, \
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

    def phonemes(self, word_lengths, word_lengths_unweighted, unstressed):
        sql_array = []
        max_word_length = len(word_lengths)
        for word_length in range(0, max_word_length):
            if len(word_lengths[word_length]) != 0:
                iterator_word_length = max_word_length if word_length == 0 else word_length
                for word_position in range(0, iterator_word_length):
                    for phoneme, next_phonemes in \
                        word_lengths[word_length][word_position].iteritems(): 
                        next_phonemes_unweighted = word_lengths_unweighted\
                            [word_length][word_position][phoneme]
                        sql_array.append("('{}', '{}', '{}', '{}', '{}', '{}')"\
                            .format(word_length,
                                    word_position,
                                    phoneme,
                                    unstressed,
                                    json.dumps(next_phonemes),
                                    json.dumps(next_phonemes_unweighted))
                        )
        sql_string = (
            "insert into phonemes (word_length, word_position, phoneme, "
            "unstressed, next_phonemes, next_phonemes_unweighted) values "
        )
        sql_string += ", ".join(sql_array)
        self.database.execute(sql_string)

    def scores(self, most_probable_words, options):
        if len(most_probable_words) == 0:
            return
        else:
            sql_array = []
            for word, score, length in most_probable_words:
                sql_array.append(
                    "('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".\
                    format(word, score, length, *options)
                )
            sql_string = (
                "insert into scores (word, score, length, ignore_position, "
                "unstressed, unweighted, method_mean, method_addition) "
                "values "
            )
            sql_string += ", ".join(sql_array)
            self.database.execute(sql_string)

    def finish(self):
        self.database.disconnect()
