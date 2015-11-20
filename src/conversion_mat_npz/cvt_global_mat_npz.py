# OS library
import os
from os.path import join
# SYS library
import sys
# Scientific library
import scipy.io as sio
import numpy as np
import pandas as pd
# Joblib library
### Module to performed parallel processing
from joblib import Parallel, delayed
# Multiprocessing library
import multiprocessing


#######################################################################
## Define a parallel function to convert each file

def cvt2npz(f, str_f):

    # Open the file
    file_mat = sio.loadmat(f)

    # Extract the data
    data = file_mat['Histogram']

    # We can convert everything into a nice numpy array
    vol_lbp_top_hist = np.array(np.squeeze(data))

    # Save the npz file
    np.savez(str_f, vol_lbp_top_hist=vol_lbp_top_hist)

#######################################################################


# Get the input arguments
radius = sys.argv[1]
data_folder = sys.argv[2]
store_folder = sys.argv[3]

# Read the csv file with the ground truth
gt_csv_filename = '/work/le2i/gu5306le/retinopathy/OCT/SERI/data.csv'
gt_csv = pd.read_csv(gt_csv_filename)
gt = gt_csv.values

# Get the good extension
data_filename = gt[:, 0]
store_filename = np.array([join(store_folder, f + '_nlm_flatten_lbp_' + str(radius) + '_hist.npz')
                          for f in data_filename])
data_filename = np.array([join(data_folder, f + '_nlm_lbptop_' + str(radius) + '_hist.mat')
                          for f in data_filename])

Parallel(n_jobs=32)(delayed(cvt2npz)(df, sf)
                    for df, sf in zip(data_filename, store_filename))
