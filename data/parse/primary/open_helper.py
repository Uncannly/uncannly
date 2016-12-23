import os
pwd = os.path.dirname(__file__)

def open_primary_data_file(filename):
  return open(os.path.join(pwd, '..', '..', '..', 'data', 'primary_data', \
  	  '{}.txt'.format(filename)), 'r')