from math import floor, log10
from copy import copy
from json import dumps
from ast import literal_eval

def kebab_to_snake(string):
    return string.replace('-', '_')

def snake_to_kebab(string):
    return string.replace('_', '-')

def kebab_to_space(string):
    return string.replace('-', ' ')

def snake_to_space(string):
    return string.replace('_', ' ')

def to_sig_figs(num, figs):
    return round(num, -int(floor(log10(num))) + (figs - 1))

def array_to_string(word, ignore_syllables):
    if ignore_syllables:
        return ' '.join(word)
    return ' '.join([' '.join(syllable) for syllable in word])

def string_to_array(word):
    return word.split(' ')

def sparse(nonsparse, desired_index, initial_value):
    while desired_index + 1 > len(nonsparse):
        nonsparse.append(copy(initial_value))

def serialize(data, ignore_syllables):
    if ignore_syllables:
        return ' '.join(data)
    return dumps(data).replace("'", "''")

def deserialize(data, ignore_syllables):
    deserializer = string_to_array if ignore_syllables else literal_eval
    return deserializer(data)

def prepare_stress_pattern(stress_pattern, unstressed):
    stress_pattern = ['start_word'] + list(stress_pattern) + ['end_word']
    if unstressed:
        stress_pattern = ['ignore_stress'] * len(stress_pattern)
    return stress_pattern