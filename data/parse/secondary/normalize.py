import operator

from lib.options import OPTION_VALUES
from lib.conversion import sparse

def stress_pattern_distributions(stress_pattern_distributions_absolute):
    normalized_stress_pattern_distributions = {}
    for weighting in OPTION_VALUES['weighting']:
        sorted_stress_pattern_distributions = sorted(
            stress_pattern_distributions_absolute[weighting].items(), 
            key=operator.itemgetter(1), reverse=True)
        normalized_stress_pattern_distributions.setdefault(weighting, [])
        total = float(sum([stress_pattern[1] for stress_pattern \
            in sorted_stress_pattern_distributions]))
        for stress_pattern in sorted_stress_pattern_distributions:
            normalized_stress_pattern_distributions[weighting].append(
                (stress_pattern[0], stress_pattern[1] / total))

    return normalized_stress_pattern_distributions

# pylint: disable=too-many-nested-blocks
def syllable_chains(syllable_chains_absolute):
    normalized_syllable_chains = {}
    for weighting in OPTION_VALUES['weighting']:
        normalized_syllable_chains.setdefault(weighting, [])

        for length in range(0, len(syllable_chains_absolute[weighting])):
            sparse(normalized_syllable_chains[weighting], length, [])

            for position in range(0, len(syllable_chains_absolute[weighting][length])):
                sparse(normalized_syllable_chains[weighting][length], position, {})

                for syllable_stress_level in syllable_chains_absolute[weighting]\
                    [length][position].keys():
                    normalized_syllable_chains[weighting][length][position]\
                        .setdefault(syllable_stress_level, {})

                    for next_syllable_stress_level in syllable_chains_absolute[weighting]\
                        [length][position][syllable_stress_level].keys():
                        normalized_syllable_chains[weighting][length][position]\
                            [syllable_stress_level].setdefault(next_syllable_stress_level, {})

                        for syllable, next_syllables in syllable_chains_absolute\
                            [weighting][length][position]\
                            [syllable_stress_level][next_syllable_stress_level].iteritems():
                            normalized_syllable_chains[weighting][length][position]\
                                [syllable_stress_level][next_syllable_stress_level].\
                                setdefault(syllable, {})

                            total = float(sum(next_syllables.itervalues()))

                            for next_syllable, probability in next_syllables.iteritems():
                                normalized_syllable_chains[weighting][length][position]\
                                    [syllable_stress_level][next_syllable_stress_level]\
                                    [syllable][next_syllable] = probability / total

    return normalized_syllable_chains
# pylint: enable=too-many-nested-blocks

def word_length_distributions(word_length_distributions_absolute):
    for weighting in OPTION_VALUES['weighting']:
        absolute_total_weight = word_length_distributions_absolute[weighting][0]
        for word_length in range(0, len(word_length_distributions_absolute[weighting])):
            word_length_distributions_absolute[weighting][word_length] /= float(absolute_total_weight)

    return word_length_distributions_absolute

def phoneme_chains(phoneme_chains_absolute):
    word_lengths = []
    for word_length, word_positions in enumerate(phoneme_chains_absolute):
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
