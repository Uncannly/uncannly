import unittest
from mock import MagicMock, patch, mock

from nose_focus import focus

from lib.modes.top_mode import TopMode

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

@mock.patch('lib.modes.top_mode.load_scores', load_scores_patch)
@mock.patch('lib.modes.top_mode.for_web', for_web_patch)
@mock.patch('lib.modes.top_mode.POOL_DEFAULT', 3)
class TopModeTest(unittest.TestCase):
    def test_happy_path(self):
        assert TopMode({}).get() == [
            ('ER1 G OW0', 0.5),
            ('OW1 L IH0 M', 0.3),
            ('AY1 K', 0.2)
        ]

    def test_selection(self):
        subject = TopMode({'selection': 2})

        randomization_evident = False
        for i in range(0, 100):
            results = subject.get()
            if results[0] != ('ER1', 0.5):
                randomization_evident = True
            assert ('AH1', 0.1) not in results
            assert len(results) == 2
        assert randomization_evident

    def test_score_threshold(self):
        assert TopMode({'score_threshold': 0.25}).get() == [
            ('ER1 G OW0', 0.5),
            ('OW1 L IH0 M', 0.3),
            'Fewer words met criteria than the specified return count.\n'
        ]

    def test_length_bounds(self):
        assert TopMode({'min_length': 2, 'max_length': 3}).get() == [
            ('ER1 G OW0', 0.5),
            ('AY1 K', 0.2),
            'Fewer words met criteria than the specified return count.\n'
        ]