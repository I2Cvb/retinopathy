""" Base code for dataset conversion and management

This code contains:
    - core functions
    - asserting definitions to ensure dataset's integrity

TODO
----
    #TODO: find the best way to define the global path
    #TODO: check tests
    #TODO: think if it should be a class in this manner 'dataset_name' etc..
           would take advantage of polimorphism and I can factorize code as
           function decorators

"""

# Authors: Joan Massich and Guillaume Lemaitre
# License: MIT

from os.path import join, exists
from os import makedirs
try:
    # Python 2
    from urllib2 import urlretrieve
except ImportError:
    # Python 3+
    from urllib import urlretrieve

from sklearn.utils.testing import assert_true





PROJECT_DATA_PATH = '../data/raw/' # it assumes that code is executed from $PROJECT/src

def get_data_home(data_home=None):
    """ Return the path to the experiment's data dir.

    This folder used to avoid repetitive downloads of the dataset
    is placed at '$PROJECT_DRI/data/raw/'

    If the folder does not already exist, it is automatically created.

    This function is a wrapper of `sklearn.datasets.get_data_home`
    """
    from sklearn.datasets import get_data_home as gdh

    return gdh(data_home=PROJECT_DATA_PATH)

def get_dataset_home(data_home=None, dir=None):
    return join(get_data_home(data_home=data_home), dir)

def check_fetch_data(dataset_raw_home=None,
                     base_url='',
                     target_filenames=[],
                     dataset_name='',
                     download_if_missing=True):
    """ Helper function for downloading any missing data of the dataset.

    Parameters
    ----------
    dataset_raw_home : Specify the folder for downloading the data of the
        dataset.  the original datasets for this `data_balance` study are 
        stored at `../data/raw/` subfolders.

    base_url: string containing the base url for fetching.

    target_filenames: list of the files that need to be download.

    download_if_missing: optional, True by default
        If False, raise a IOError if the data is not locally available
        instead of trying to download the data from the source site.

    #TODO: create a test for download_if_missing
    """
    #TODO: assert url directory
    #TODO: assert no empty list

    if not exists(dataset_raw_home):
        makedirs(dataset_raw_home)
    for target in target_filenames:
        path = join(dataset_raw_home, target)
        if not exists(path):
            if download_if_missing:
                full_url = join(base_url, target)
                print('downloading %s data from %s to %s' %
                    (RAW_DATA_LABEL, full_url, dataset_raw_home))
                urlretrieve(full_url, path)
            else:
                raise IOError('%s is missing' % path)

def check_data(data):
    check_data_type(data)
    check_no_missing_data(data)




def check_label(label):
    check_label_type(label)
    check_two_class_only(label)




def check_no_missing_data(data):
    #TODO
    assert_true(True)

def check_two_class_only(label):
    #TODO
    assert_true(True)

def check_data_type(data):
    assert_true(data.dtype == np.int)


def check_label_type(label):
    assert_true(label.dtype == np.int)


def main():
    print 'this is base.py'
    # from tests.test_base import main as xx
    # xx()

if __name__ == '__main__':
    main()
