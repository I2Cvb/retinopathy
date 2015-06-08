""" The FREAKING AWESOME name of our dataset

Brief description
-----------------

Original Owner and Donor
------------------------
#TODO

References
----------

"""

# Authors: Joan Massich and Guillaume Lemaitre
# License: MIT

import data_loading

# Grab the module-level docstring to use as a description of the
# dataset
MODULE_DOCS = __doc__

DATA_URL = "https://depot.u-bourgogne.fr/?dlid=2797aa30b7fef39a0ef01ba2c0cc332c"
TARGET_FILENAME_ = ["data.zip"]
RAW_DATA_LABEL = 'oct'


def fetch_oct(download_if_missing=True):
    """Fetcher for the ******* dataset.

    Parameters
    ----------
    download_if_missing: optional, True by default
        If False, raise a IOError if the data is not locally available
        instead of trying to download the data from the source site.

    """
    dataset_raw_home = get_dataset_home(dir=RAW_DATA_LABEL)
    check_fetch_data(dataset_raw_home=dataset_raw_home,
                     base_url=DATA_URL,
                     target_names=TARGET_FILENAME_,
                     dataset_name=RAW_DATA_LABEL,
                     download_if_missing=download_if_missing
                     )


def process_oct():
    """Process data of the **********dataset.

    it generates a npz according to... #TODO

    #TODO: check if files exist
    #TODO: a generic file managing using get_data_home
    #TODO:
    """

    return (np.append(ticdata[:,:-1], ticeval, axis=0),
            np.append(ticdata[:,-1], tictgts, axis=0))

def check_dataset(data):
    check_data(data)

def check_gt(label):
    check_label(label)

def convert_oct():
    fetch_oct(download_if_missing=True)
    d, l = process_oct()
    check_dataset(d)
    check_gt(l)
    #TODO: change this hardcoded file
    np.savez('../data/clean/oct.npz', data=d, label=l)

def load_oct():
    raise NotImplementedError()

if __name__ == '__main__':
    convert_oct()
