import unittest
# pylint: disable=import-error
from mock import patch

# pylint: disable=unused-import
from nose_focus import focus
# pylint: enable=unused-import,import-error

from lib.phonemes.top_mode import TopModePhonemes

# pylint: disable=unused-argument
def for_web_patch(result, *args):
    word, score = result
    return ' '.join(word), score

def load_scores_patch(*args):
    return [
        ('AH1', 0.1),
        ('AY1 K', 0.2),
        ('ER1 G OW0', 0.5),
        ('OW1 L IH0 M', 0.3)
    ]
# pylint: enable=unused-argument

# pylint: disable=no-self-use
@patch('lib.phonemes.top_mode.load_scores', load_scores_patch)
@patch('lib.phonemes.top_mode.for_web', for_web_patch)
@patch('lib.phonemes.top_mode.POOL_DEFAULT', 3)
class TopModePhonemesTest(unittest.TestCase):
    def test_happy_path(self):
        assert TopModePhonemes({}).get() == [
            ('ER1 G OW0', 0.5),
            ('OW1 L IH0 M', 0.3),
            ('AY1 K', 0.2)
        ]

    def test_selection(self):
        subject = TopModePhonemes({'selection': 2})

        randomization_evident = False
        for _ in range(0, 100):
            results = subject.get()
            if results[0] != ('ER1', 0.5):
                randomization_evident = True
            assert ('AH1', 0.1) not in results
            assert len(results) == 2
        assert randomization_evident

    def test_score_threshold(self):
        assert TopModePhonemes({'score_threshold': 0.25}).get() == [
            ('ER1 G OW0', 0.5),
            ('OW1 L IH0 M', 0.3),
            'Fewer words met criteria than the specified return count.\n'
        ]

    def test_length_bounds(self):
        assert TopModePhonemes({'min_length': 2, 'max_length': 3}).get() == [
            ('ER1 G OW0', 0.5),
            ('AY1 K', 0.2),
            'Fewer words met criteria than the specified return count.\n'
        ]
# pylint: enable=no-self-use
