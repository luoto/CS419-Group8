import unittest
import sys
sys.path.append('../utils')
import utils

class TestUtils(unittest.TestCase):

    def test_arrayify(self):
        self.assertEqual(utils.arrayify('Hello World'), ['Hello', 'Worlds'])

if __name__ == '__main__':
    unittest.main()
