#title           :extraction_codebook.py
#description     :This will create a header for a python script.
#author          :Guillaume Lemaitre
#date            :2015/06/07
#version         :0.1
#notes           :
#python_version  :2.7.6  
#==============================================================================

# Import the needed libraries
# Numpy library
import numpy as np
# Panda library
import pandas as pd
# OS library
import os
from os.path import join
# SYS library
import sys
# Joblib library
### Module to performed parallel processing
from joblib import Parallel, delayed
# Multiprocessing library
import multiprocessing

from protoclass.extraction.codebook import *

#########################################################################
### Definition of the parallel codebook

def CBComputation(idx_test, (pat_test_norm, pat_test_dme),
                  filename_normal, filename_dme, nw):

    pat_train_norm = np.delete(filename_normal, idx_test)
    pat_train_dme = np.delete(filename_dme, idx_test)

    # Open the current training data
    training_data = np.concatenate((np.concatenate([get_lbp_data(f) for f in pat_train_norm],
                                                   axis=0),
                                    np.concatenate([get_lbp_data(f) for f in pat_train_dme],
                                                   axis=0)), 
                                   axis=0)

    print 'The size of the training dataset is {}'.format(training_data.shape)

    # Create the codebook using the training data
    num_cores = 8
    cbook = [CodeBook(n_words=w, init='k-means++', n_jobs=num_cores, n_init=5)
             for w in nw]

    # Fit each code book for the data currently open
    for idx_cb, c in enumerate(cbook):
        print 'Fitting for dictionary with {} words'.format(nw[idx_cb])
        c.fit(training_data)

    return cbook

################################################################################################

################################################################################################
# Define the number of words 
nb_words = [int(sys.argv[3])]

################################################################################################

# Read the csv file with the ground truth
gt_csv_filename = '/work/le2i/gu5306le/retinopathy/OCT/SERI/data.csv'
gt_csv = pd.read_csv(gt_csv_filename)

gt = gt_csv.values

data_filename = gt[:, 0]

# Get the good extension
radius = sys.argv[1]
data_filename = np.array([f + '_nlm_flatten_lbp_' + str(radius) + '_hist.npz' for f in data_filename])

label = gt[:, 1]
label = ((label + 1.) / 2.).astype(int)

from collections import Counter
    
count_gt = Counter(label)

if (count_gt[0] != count_gt[1]):
    raise ValueError('Not balanced data.')
else:
    # Split data into positive and negative
    # TODO TACKLE USING PERMUTATION OF ELEMENTS
    filename_normal = data_filename[label == 0]
    filename_dme = data_filename[label == 1]

    # Get the input folder where the information are located
    input_folder = sys.argv[2]
    # Build the data folder from the radius given
    data_folder = join(input_folder, 'r_' + str(radius) + '_hist_npz')

    # Open the data
    ### Features
    get_lbp_data = lambda f: np.load(join(data_folder, f))['vol_lbp_hist']

    # Compute a codebook for each fold
    codebook_list = []
    for idx_test, (pat_test_norm, pat_test_dme) in enumerate(zip(filename_normal, filename_dme)):
        codebook_list.append(CBComputation(idx_test, (pat_test_norm, pat_test_dme),
                                           filename_normal, filename_dme, nb_words))

    # We have to store the final codebook
    # Give the location of the random codebook previously generated
    codebook_type = 'codebook_final'
    codebook_path = join(data_folder, codebook_type)
    codebook_filename = join(codebook_path, 'codebook.pkl')
    if not os.path.exists(codebook_path):
        os.makedirs(codebook_path)

    from sklearn.externals import joblib
    joblib.dump(codebook_list, codebook_filename)
