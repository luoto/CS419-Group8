import unittest
import curse_db.utils as utils

class TestUtils(unittest.TestCase):

    def test_arrayify(self):
        self.assertEqual(utils.arrayify('Hello World'), ['Hello', 'World'])

if __name__ == '__main__':
    unittest.main()
