import sys
import json

from lib.options import option_value_string_to_boolean, SCORING_METHODS

class Tables(object):
    def __init__(self, database):
        self.database = database

    def schema(self):
        sql_array = [
            "drop table if exists words",
            "create table words (word varchar, pronunciation varchar, frequency int)",
            "drop table if exists phonemes",
            "create table phonemes (word_length int, word_position int, \
              phoneme varchar, unstressed boolean, next_phonemes_weighted varchar, \
              next_phonemes_unweighted varchar)",
            "drop table if exists syllables",
            "create table syllables (word_length int, word_position int, \
              stressing varchar, next_stressing varchar, syllable varchar, \
              next_syllables_weighted varchar, next_syllables_unweighted varchar)",
            "drop table if exists scores",
            "create table scores (word varchar, score real, length int, \
              ignore_position boolean, unstressed boolean, unweighted boolean, \
              method_mean boolean, method_addition boolean, ignore_syllables boolean)",
            ""
        ]
        sql_string = ";".join(sql_array)
        self.database.execute(sql_string)
        sys.stdout.write('Tables created.\n\n')

    def words(self, words):
        sql_array = []
        for word, pronunciation, frequency in words:
            sql_array.append("('{}', '{}', '{}')".format(
                word.replace("'", "''"), pronunciation, frequency
            ))
        sql_string = "insert into words (word, pronunciation, frequency) values "
        sql_string += ", ".join(sql_array)
        self.database.execute(sql_string)
        sys.stdout.write('Words table populated.\n\n')

    def syllables(self, syllables):
        sql_array = []
        syllables_unweighted = syllables['unweighted']
        syllables = syllables['weighted']
        for word_length in range(0, len(syllables)):
            for word_position in range(0, len(syllables[word_length])): # do i need a + 1 here?
                for previous_stressing, next_stressings in \
                    syllables[word_length][word_position].iteritems():
                    for next_stressing, previous_syllables in next_stressings.iteritems():
                        for previous_syllable, next_syllables in previous_syllables.iteritems():
                            next_syllables_unweighted = syllables_unweighted[word_length]\
                                [word_position][previous_stressing][next_stressing]\
                                [previous_syllable]
                            next_syllables_unweighted = \
                                {str(k).replace("'", '"'): v for k, v \
                                in next_syllables_unweighted.iteritems()}
                            next_syllables = {str(k).replace("'", '"'): v for k, v \
                                in next_syllables.iteritems()}
                            sql_array.append("('{}', '{}', '{}', '{}', '{}', '{}', '{}')"\
                                .format(word_length,
                                        word_position,
                                        previous_stressing,
                                        next_stressing,
                                        str(previous_syllable).replace("'", "''"),
                                        json.dumps(next_syllables).replace('"', "''"),
                                        json.dumps(next_syllables_unweighted).replace('"', "''")))
            if word_length == 0:
                sys.stdout.write('Syllable chain table all positions for ignore length updated.\n')
            else:
                sys.stdout.write(('Syllable chain table all positions for length '
                                  '{} updated.\n').format(word_length))
        sql_string = (
            "insert into syllables (word_length, word_position, stressing, next_stressing, "
            "syllable, next_syllables_weighted, next_syllables_unweighted) values "
        )
        sql_string += ", ".join(sql_array)
        self.database.execute(sql_string)

    def phonemes(self, word_lengths_weighted, word_lengths_unweighted, stressing):
        sql_array = []
        max_word_length = len(word_lengths_weighted)
        unstressed = option_value_string_to_boolean(stressing)
        for word_length in range(0, max_word_length):
            if len(word_lengths_weighted[word_length]) != 0:
                iterator_word_length = max_word_length if word_length == 0 else word_length
                for word_position in range(0, iterator_word_length):
                    for phoneme, next_phonemes_weighted in \
                        word_lengths_weighted[word_length][word_position].iteritems():
                        next_phonemes_unweighted = word_lengths_unweighted\
                            [word_length][word_position][phoneme]
                        sql_array.append("('{}', '{}', '{}', '{}', '{}', '{}')"\
                            .format(word_length,
                                    word_position,
                                    phoneme,
                                    unstressed,
                                    json.dumps(next_phonemes_weighted),
                                    json.dumps(next_phonemes_unweighted)))
            if word_length == 0:
                sys.stdout.write(('Phoneme chain table all positions for ignore length '
                                  '{} updated.\n').format(stressing))
            else:
                sys.stdout.write(('Phoneme chain table all positions for length '
                                  '{} {} updated.\n').format(word_length, stressing))
        sql_string = (
            "insert into phonemes (word_length, word_position, phoneme, "
            "unstressed, next_phonemes_weighted, next_phonemes_unweighted) values "
        )
        sql_string += ", ".join(sql_array)
        self.database.execute(sql_string)

    def scores(self, most_probable_words, options):
        boolean_options = string_to_boolean(options)

        if len(most_probable_words) == 0:
            return
        else:
            sql_array = []
            for word, score, length in most_probable_words:
                sql_array.append(
                    "('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".\
                    format(word, score, length, *boolean_options)
                )
            sql_string = (
                "insert into scores (word, score, length, ignore_position, "
                "unstressed, unweighted, method_mean, method_addition, ignore_syllables) "
                "values "
            )
            sql_string += ", ".join(sql_array)
            self.database.execute(sql_string)

    def finish(self):
        self.database.disconnect()

def string_to_boolean(options):
    positioning, stressing, weighting, scoring_method, ignore_syllables = options
    ignore_position = option_value_string_to_boolean(positioning)
    unstressed = option_value_string_to_boolean(stressing)
    unweighted = option_value_string_to_boolean(weighting)
    method_mean, method_addition = SCORING_METHODS[scoring_method]
    return ignore_position, unstressed, unweighted, method_mean, method_addition, ignore_syllables
