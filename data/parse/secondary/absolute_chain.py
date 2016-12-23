class AbsoluteChain(object):
  @staticmethod
  def parse(phoneme_chain_absolute):
    this_phonemes_next_phonemes = {}

    for phoneme, next_phoneme_counts in phoneme_chain_absolute.iteritems():
      this_phonemes_next_phonemes[phoneme] = next_phonemes(next_phoneme_counts)

    return this_phonemes_next_phonemes

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
