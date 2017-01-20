import sys
from json import dumps

from lib.options import option_value_string_to_boolean, option_value_boolean_to_string, \
    SCORING_METHODS
from lib.conversion import snake_to_space, serialize, deep_serialize


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
              stress varchar, next_stress varchar, syllable varchar, \
              next_syllables_weighted varchar, next_syllables_unweighted varchar)",
            "drop table if exists scores",
            "create table scores (word varchar, score real, length int, \
              ignore_position boolean, unstressed boolean, unweighted boolean, \
              method_mean boolean, method_addition boolean, ignore_syllables boolean)",
            ""
        ]
        sql_string = ";".join(sql_array)
        self.database.execute(sql_string)

    def words(self, words):
        sql_array = []
        for word, pronunciation, frequency in words:
            sql_array.append("('{}', '{}', '{}')".format(
                serialize(word, ignore_syllables=False), pronunciation, frequency
            ))
        sql_string = "insert into words (word, pronunciation, frequency) values "
        sql_string += ", ".join(sql_array)
        self.database.execute(sql_string)

    def syllables(self, syllables):
        sql_array = []
        syllables_unweighted = syllables['unweighted']
        syllables_weighted = syllables['weighted']
        for word_length in range(0, len(syllables_weighted)):
            for word_position in range(0, len(syllables_weighted[word_length])):
                for stress, next_stresses in \
                    syllables_weighted[word_length][word_position].iteritems():
                    for next_stress, syllables in next_stresses.iteritems():
                        for syllable, next_syllables in syllables.iteritems():
                            next_syllables_unweighted = syllables_unweighted[word_length]\
                                [word_position][stress][next_stress][syllable]

                            sql_array.append("('{}', '{}', '{}', '{}', '{}', '{}', '{}')"\
                                .format(word_length,
                                        word_position,
                                        stress,
                                        next_stress,
                                        serialize(syllable, ignore_syllables=False),
                                        deep_serialize(next_syllables),
                                        deep_serialize(next_syllables_unweighted)))
            if word_length == 0:
                sys.stdout.write('Syllable chain table all positions for ignore length updated.\n')
            else:
                sys.stdout.write(('Syllable chain table all positions for length '
                                  '{} updated.\n').format(word_length))
        sql_string = (
            "insert into syllables (word_length, word_position, stress, next_stress, "
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
                                    dumps(next_phonemes_weighted),
                                    dumps(next_phonemes_unweighted)))
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

    # pylint: disable=too-many-locals
    def scores(self, most_probable_words, options):
        positioning, stressing, weighting, scoring_method, length_consideration, \
            ignore_syllables = options
        boolean_options = string_to_boolean(positioning, stressing, weighting,
                                            scoring_method, ignore_syllables)

        if len(most_probable_words) == 0:
            return
        else:
            sql_array = []
            for word, score, length in most_probable_words:
                sql_array.append(
                    "('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".\
                    format(serialize(word, ignore_syllables), score, length, *boolean_options)
                )
            sql_string = (
                "insert into scores (word, score, length, ignore_position, "
                "unstressed, unweighted, method_mean, method_addition, ignore_syllables) "
                "values "
            )
            sql_string += ", ".join(sql_array)
            self.database.execute(sql_string)

            syllable_use = option_value_boolean_to_string('syllable_use', ignore_syllables)
            sys.stdout.write('Most probable words {} {} {} {} {} {} done.\n'.format(
                snake_to_space(stressing),
                snake_to_space(weighting),
                snake_to_space(length_consideration),
                snake_to_space(positioning),
                snake_to_space(scoring_method),
                snake_to_space(syllable_use)))
    # pylint: enable=too-many-locals

    def finish(self):
        self.database.disconnect()

def string_to_boolean(positioning, stressing, weighting, scoring_method, ignore_syllables):
    ignore_position = option_value_string_to_boolean(positioning)
    unstressed = option_value_string_to_boolean(stressing)
    unweighted = option_value_string_to_boolean(weighting)
    method_mean, method_addition = SCORING_METHODS[scoring_method]
    return ignore_position, unstressed, unweighted, method_mean, method_addition, ignore_syllables
