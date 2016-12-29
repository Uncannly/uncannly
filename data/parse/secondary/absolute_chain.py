def parse(phoneme_chain_absolute):
    word_lengths = []
    for word_length, word_positions in enumerate(phoneme_chain_absolute):
        word_lengths.append([])
        for word_position in word_positions:
            this_phonemes_next_phonemes = {}
            for phoneme, next_phoneme_counts in word_position.iteritems():
                this_phonemes_next_phonemes[phoneme] = next_phonemes(next_phoneme_counts)
            word_lengths[word_length].append(this_phonemes_next_phonemes)

    return word_lengths

def next_phonemes(next_phoneme_counts):
    phonemes = sorted(
        next_phoneme_counts,
        key=next_phoneme_counts.get,
        reverse=True
    )

    total_next_phonemes = sum(next_phoneme_counts.itervalues())
    results = []
    for phoneme in phonemes:
        next_counts = next_phoneme_counts[phoneme]
        results.append((phoneme, float(next_counts) / float(total_next_phonemes)))
    return results
