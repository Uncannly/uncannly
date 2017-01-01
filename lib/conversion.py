from math import floor, log10

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
