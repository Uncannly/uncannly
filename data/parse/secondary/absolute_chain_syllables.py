from lib.options import OPTION_VALUES
from lib.conversion import sparse

# pylint: disable=too-many-nested-blocks
def parse(syllable_chains):
    normalized_syllable_chains = {}
    for weighting in OPTION_VALUES['weighting']:
        normalized_syllable_chains.setdefault(weighting, [])

        for length in range(0, len(syllable_chains[weighting])):
            sparse(normalized_syllable_chains[weighting], length, [])

            for position in range(0, len(syllable_chains[weighting][length])):
                sparse(normalized_syllable_chains[weighting][length], position, {})

                for syllable_stress_level in syllable_chains[weighting][length][position].keys():
                    normalized_syllable_chains[weighting][length][position]\
                        .setdefault(syllable_stress_level, {})

                    for next_syllable_stress_level in syllable_chains[weighting][length][position][syllable_stress_level].keys():
                        normalized_syllable_chains[weighting][length][position]\
                            [syllable_stress_level].setdefault(next_syllable_stress_level, {})

                        for syllable, next_syllables in syllable_chains[weighting][length][position]\
                            [syllable_stress_level][next_syllable_stress_level].iteritems():
                            normalized_syllable_chains[weighting][length][position]\
                                [syllable_stress_level][next_syllable_stress_level].setdefault(syllable, {})

                            total = float(sum(next_syllables.itervalues()))

                            for next_syllable, probability in next_syllables.iteritems():
                                normalized_syllable_chains[weighting][length][position]\
                                    [syllable_stress_level][next_syllable_stress_level]\
                                    [syllable][next_syllable] = probability / total

    return normalized_syllable_chains
# pylint: enable=too-many-nested-blocks,line-too-long,invalid-name
