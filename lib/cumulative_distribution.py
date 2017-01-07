from random import random

def choose_next(iterable, callback, callback_arguments):
    random_number = random()
    accumulated_probability = 0
    for item, probability in iterable:
        accumulated_probability += probability
        if accumulated_probability > random_number:
            return callback(item, probability, callback_arguments)
