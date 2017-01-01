# pylint: disable=too-few-public-methods

def parse(phoneme_chain_absolute):
    word_lengths = []
    for word_length, word_positions in enumerate(phoneme_chain_absolute):
        word_lengths.append([])
        for word_position in word_positions:
            next_phonemes = {}
            for phoneme, next_counts in word_position.iteritems():
                next_phonemes[phoneme] = _next_phonemes(next_counts)
            word_lengths[word_length].append(next_phonemes)

    return word_lengths

def _next_phonemes(next_counts):
    phonemes = sorted(next_counts, key=next_counts.get, reverse=True)
    total_next = sum(next_counts.itervalues())
    return [_normalize(phoneme, next_counts, total_next) for phoneme in phonemes]

def _normalize(phoneme, next_counts, total_next):
    return phoneme, float(next_counts[phoneme]) / float(total_next)

# pylint: enable=too-few-public-methods
