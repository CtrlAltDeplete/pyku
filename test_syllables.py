from syllables import *
import unittest
from ddt import ddt
from ddt import file_data


@ddt
class TestSyllables(unittest.TestCase):
    @file_data('testdata.txt')
    def test_word(self, testData):
        print(testData[0])
        self.assertEqual(syllablesInWord(testData[0]), testData[1])


if __name__ == '__main__':
    unittest.main()
