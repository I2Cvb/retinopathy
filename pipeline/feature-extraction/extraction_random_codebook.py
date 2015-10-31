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

# Read the csv file with the ground truth
#gt_csv_filename = '/DATA/OCT/data_organized/data.csv'
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
    
    data_folder = sys.argv[2]

    def CBComputation(idx_test, (pat_test_norm, pat_test_dme), filename_normal, filename_dme, data_folder):

        pat_train_norm = np.delete(filename_normal, idx_test)
        pat_train_dme = np.delete(filename_dme, idx_test)

        # open the training data
        vol_name = 'vol_lbp_hist'
        training_data = np.concatenate((np.concatenate([np.load(join(data_folder, f))[vol_name] 
                                                        for f in pat_train_norm], axis=0),
                                        np.concatenate([np.load(join(data_folder, f))[vol_name] 
                                                        for f in pat_train_dme], axis=0)), 
                                       axis=0)

        # open the testing data
        print join(data_folder, pat_test_norm)
        print join(data_folder, pat_test_dme)
        testing_data = np.concatenate((np.load(join(data_folder, pat_test_norm))[vol_name], 
                                       np.load(join(data_folder, pat_test_dme))[vol_name]), 
                                      axis=0)
        
        print 'The size of the training dataset is {}'.format(training_data.shape)
        print 'The size of the testing dataset is {}'.format(testing_data.shape)
        
        # Create the codebook using the training data
        num_cores = 8
        list_n_words = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
                        200, 300, 400, 500,
                        1000]
        #cbook = [CodeBook(n_words=w, n_jobs=num_cores, n_init=5) for w in list_n_words]
        cbook = [CodeBook(n_words=w, init='random', n_jobs=num_cores, n_init=1, cluster_core='random-words')
                 for w in list_n_words]

        # Fit each code book for the data currently open
        for idx_cb, c in enumerate(cbook):
            print 'Fitting for dictionary with {} words'.format(list_n_words[idx_cb])
            c.fit(training_data)

        return cbook
            
    # codebook_list = Parallel(n_jobs=8)(delayed(CBComputation)(idx_test, (pat_test_norm, pat_test_dme), filename_normal, filename_dme, data_folder) 
    #                                    for idx_test, (pat_test_norm, pat_test_dme) in enumerate(zip(filename_normal, filename_dme)))
    codebook_list = []
    for idx_test, (pat_test_norm, pat_test_dme) in enumerate(zip(filename_normal, filename_dme)):
        codebook_list.append(CBComputation(idx_test, (pat_test_norm, pat_test_dme), filename_normal, filename_dme, data_folder))

    # We have to store the final codebook
    path_to_save = join(data_folder, 'codebook_random')
    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)

    from sklearn.externals import joblib
    joblib.dump(codebook_list, join(path_to_save, 'codebook.pkl'))
