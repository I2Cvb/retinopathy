# Get the correct unittest library
try:
    import unittest2 as unittest
except ImportError:
    import unittest

from data_conversion.base import get_data_home
# from data_conversion.base import PROJECT_DATA_PATH
# from data_conversion.base import fetch_mldata

class Test_data_convert(unittest.TestCase):

    def test_data_home(self):
        # # get_data_home will point to a pre-existing folder
        # data_home = get_data_home()
        # assert_equal(data_home, PROJECT_DATA_PATH)

        # # ensure that the folder has been created
        # assert_true(os.path.exists(data_home))
        print 'hi from the test'


def main():
    unittest.main()

if __name__ == '__main__':
    main()
