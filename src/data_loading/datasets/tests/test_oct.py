# Get the correct unittest library
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from data_loading.base import *
from data_loading.datasets.oct import *

class Test_oct(unittest.TestCase):

    def test_convert_oct(self):
        convert_oct()

def main():
    unittest.main()

if __name__ == '__main__':
    main()
