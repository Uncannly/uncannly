import os
PWD = os.path.dirname(__file__)

def open_primary_data_file(filename):
    return open(os.path.join(PWD, '..', '..', '..', 'data', 'primary_data', \
        '{}.txt'.format(filename)), 'r')
