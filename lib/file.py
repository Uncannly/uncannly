import cPickle

def load(filename):
	with open('secondary_data/{}.pkl'.format(filename), 'rb') as input:
		return cPickle.load(input)

def save(data, filename):
	with open('secondary_data/{}.pkl'.format(filename), 'wb') as output:
		cPickle.dump(data, output, -1)