import cPickle

def load(filename):
    with open('data/secondary_data/{}.pkl'.format(filename), 'rb') as data:
        return cPickle.load(data)

def save(data, filename):
    with open('data/secondary_data/{}.pkl'.format(filename), 'wb') as output:
        cPickle.dump(data, output, -1)
