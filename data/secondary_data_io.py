import cPickle

def save_word_length_distributions(distributions):
    for weighting, distribution in distributions.iteritems():
        with open('data/secondary_data/word_length_distribution_{}.pkl'.\
            format(weighting), 'wb') as output:
            cPickle.dump(distribution, output, -1)

def load_word_length_distribution(weighting):
    with open('data/secondary_data/word_length_distribution_{}.pkl'.\
        format(weighting), 'rb') as word_length_distribution:
        return cPickle.load(word_length_distribution)
