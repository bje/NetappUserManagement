__author__ = 'kmadac'

import unittest
from UserManagement.BaseFilerApi import BaseFilerApi

class Test_BaseAPI(unittest.TestCase):
    def test_test_connection(self):
        self.netappapi = BaseFilerApi('10.228.167.98', 'root', ['nasrise1', 'NasRise9', 'TSIis!'])
        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()
