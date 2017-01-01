from math import floor, log10
from copy import copy

def kebab_to_snake(string):
    return string.replace('-', '_')

def snake_to_kebab(string):
    return string.replace('_', '-')

def to_sig_figs(num, figs):
    return round(num, -int(floor(log10(num))) + (figs - 1))

def array_to_string(word):
    return ' '.join(word)

def string_to_array(word):
    return word.split(' ')

def sparse(nonsparse, desired_index, initial_value):
    while desired_index + 1 > len(nonsparse):
        nonsparse.append(copy(initial_value))
