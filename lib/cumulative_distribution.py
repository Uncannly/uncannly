from random import random

def choose_next(iterable, callback=None, callback_arguments=None):
    random_number = random()
    accumulated_probability = 0
    for item, probability in iterable:
        accumulated_probability += probability
        if accumulated_probability > random_number:
            if callback:
                return callback(item, probability, callback_arguments)
            else:
                return item
