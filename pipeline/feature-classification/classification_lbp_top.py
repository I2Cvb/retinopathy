#title           :classification_lbp_top.py
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
import scipy.io as sio  
# OS library
import os
from os.path import join
# SYS library
import sys

from protoclass.extraction.codebook import *
from protoclass.classification.classification import Classify

# Read the csv file with the ground truth
#gt_csv_filename = '/DATA/OCT/data_organized/data.csv'
gt_csv_filename = '/work/le2i/gu5306le/OCT/data.csv'
#gt_csv_filename = '/work/le2i/gu5306le/dukeOCT/data2.csv'
gt_csv = pd.read_csv(gt_csv_filename)

gt = gt_csv.values

data_filename = gt[:, 0]

# Get the good extension
radius2 = 3
radius = 24
# LBP TOP mat filename
#data_filename = np.array([f + '_nlm_' + str(radius) + 'u_LbpTop_u.mat' for f in data_filename])
data_filename = np.array([f + '_nlm_flatten_' + str(radius) + 'u_LbpTop_u.mat' for f in data_filename])

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

    # Get the right directory where the matfile are locatd
    data_folder = '/user1/le2i/gu5306le/Work/OCT_processing/features/'

    # change np.load by sp.loadmat
    # 
    #get_lbp_data = lambda f: sio.loadmat(join(data_folder, f))['Histogram'].reshape(-1)
    def get_lbp_data(f):
        fmat = sio.loadmat(join(data_folder, f))
        return np.ravel(fmat.get('Histogram'))

    results_cv = []
    for idx_test, (pat_test_norm, pat_test_dme) in enumerate(zip(filename_normal, filename_dme)):

        # Take the testing out and keep the rest for training
        pat_train_norm = np.delete(filename_normal, idx_test)
        pat_train_dme = np.delete(filename_dme, idx_test)

        # Collect the current training data
        training_normal = [get_lbp_data(f) for f in pat_train_norm]
        training_dme = [get_lbp_data(f) for f in pat_train_dme]

        # Compose the training ( data & labels )
        training_data = np.array(training_normal+training_dme)
        training_label = np.array([0]*len(training_normal) + [1]*len(training_dme), dtype=int)

        print training_data.shape
        
        # Compose the testing
        testing_data = np.array([get_lbp_data(filename_normal[idx_test]),
                                 get_lbp_data(filename_dme[idx_test])])

        print testing_data.shape
        
        # Run the classification for this specific data
        #max_features = None
        max_features = 'auto'
        pred_label, roc = Classify(training_data,
                                   training_label,
                                   testing_data,
                                   np.array([0, 1], dtype=int),
                                   classifier_str='random-forest',
                                   n_estimators=100,
                                   n_jobs=60,
                                   max_features=max_features)

        results_cv.append((pred_label, roc))

    # We have to store the final codebook
    path_to_save = '/work/le2i/gu5306le/OCT/SPIE/lbptop_nri_flatten_r_' + str(radius2) + '_results'
    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)

    from sklearn.externals import joblib
    joblib.dump(results_cv, join(path_to_save, 'hist.pkl'))
