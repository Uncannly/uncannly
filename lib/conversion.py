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

def data_to_formatted_string(data, ignore_syllables):
    formatter = _array_to_string if ignore_syllables else _deep_array_to_string
    return formatter(data)

def _string_to_array(data):
    return data.split(' ')

def _deep_array_to_string(data):
    return _array_to_string([_array_to_string(element) for element in data])

def _array_to_string(data):
    return ' '.join(data)

def _tuple_to_string(data):
    return dumps(data).replace("'", "''")

def sparse(nonsparse, desired_index, initial_value):
    while desired_index + 1 > len(nonsparse):
        nonsparse.append(copy(initial_value))

def serialize(data, ignore_syllables):
    serializer = _array_to_string if ignore_syllables else _tuple_to_string
    return serializer(data)

def deep_serialize(data):
    data = {serialize(k, ignore_syllables=False): v for k, v in data.iteritems()}
    return serialize(data, ignore_syllables=False)

def deserialize(data, ignore_syllables):
    deserializer = _string_to_array if ignore_syllables else literal_eval
    return deserializer(data)

def deep_deserialize(data):
    data = deserialize(data, ignore_syllables=False)
    return {deserialize_and_hashablize(k): v for k, v in data.iteritems()}

def deserialize_and_hashablize(data):
    return tuple(literal_eval(data))

def prepare_stress_pattern(stress_pattern, unstressed):
    stress_pattern = ['start_word'] + list(stress_pattern) + ['end_word']
    if unstressed:
        stress_pattern = ['ignore_stress'] * len(stress_pattern)
    return stress_pattern