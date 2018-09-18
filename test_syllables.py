from syllables import *
import unittest


class TestSyllables(unittest.TestCase):
    words_to_test = {
        'utterly': 3,
        'vacuum': 2,
        'spoil': 2,
        'ruin': 2,
        'civil': 2,
        'service': 2,
        'looking': 2,
        'specified': 3
    }

    def test_word(self):
        for key, value in self.words_to_test.items():
            print(key)
            self.assertEqual(syllablesInWord(key), value)


if __name__ == '__main__':
    unittest.main()
