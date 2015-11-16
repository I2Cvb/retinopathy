#title           :classification_lbp_local_random.py
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
from protoclass.classification.classification import Classify


#########################################################################
### Definition of the parallel classification

def ParallelClassification(idx_test, (pat_test_norm, pat_test_dme),
                           filename_normal, filename_dme,
                           data_folder, nw, cb_list, config_class):


    # Take the testing out and keep the rest for training
    pat_train_norm = np.delete(filename_normal, idx_test)
    pat_train_dme = np.delete(filename_dme, idx_test)

    results_by_codebook = []
    for idx_words, current_cbook in enumerate(cb_list[idx_test]):

        print 'Analysis of the the codebook with {} words'.format(nw[idx_words])

        # Collect the current training data
        training_normal = [current_cbook.get_BoF_descriptor(get_lbp_data(f))[0] for f in pat_train_norm]
        training_dme = [current_cbook.get_BoF_descriptor(get_lbp_data(f))[0] for f in pat_train_dme]

        # Compose the training ( data & labels )
        training_data = np.array(training_normal+training_dme)
        training_label = np.array([0]*len(training_normal) + [1]*len(training_dme), dtype=int)

        # Compose the testing
        testing_data = np.array([current_cbook.get_BoF_descriptor(get_lbp_data(filename_normal[idx_test]))[0],
                                 current_cbook.get_BoF_descriptor(get_lbp_data(filename_dme[idx_test]))[0]])

        # Run the classification for this specific data
        pred_label, roc = Classify(training_data,
                                   training_label,
                                   testing_data,
                                   np.array([0, 1], dtype=int),
                                   **config_class)

        results_by_codebook.append((pred_label, roc))

    return results_by_codebook

################################################################################################

################################################################################################
### Define the global variable regarding the classification

config = [{'classifier_str' : 'random-forest', 'n_estimators' : 100, 'gs_n_jobs' : 8},
          {'classifier_str' : 'knn', 'n_neighbors' : 3, 'gs_n_jobs' : 8},
          {'classifier_str' : 'knn', 'n_neighbors' : 5, 'gs_n_jobs' : 8},
          {'classifier_str' : 'knn', 'n_neighbors' : 7, 'gs_n_jobs' : 8},
          {'classifier_str' : 'logistic-regression', 'gs_n_jobs' : 8},
          {'classifier_str' : 'kernel-svm', 'gs_n_jobs' : 8},
          {'classifier_str' : 'gradient-boosting', 'n_estimators' : 100, 'gs_n_jobs' : 8}]

# Define the number of words 
nb_words = [10, 20, 30, 40, 50, 60, 70, 80, 90,
            100, 200, 300, 400, 500,
            1000, 2000, 3000, 4000, 5000]

################################################################################################

################################################################################################
### Build the GT

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
    # Give the location of the random codebook previously generated
    codebook_type = 'codebook_random'
    codebook_filename = join(data_folder, join(codebook_type, 'codebook.pkl'))

    # Open the data
    ### Features
    get_lbp_data = lambda f: np.load(join(data_folder, f))['vol_lbp_hist']
    from sklearn.externals import joblib
    ### Codebook
    codebook_list = joblib.load(codebook_filename)

    # Make the classification for each configuration
    result_config = []    
    for c in config:
        print c

        results_cv = Parallel(n_jobs=1)(delayed(ParallelClassification)(idx_test, (pat_test_norm, pat_test_dme),
                                                                        filename_normal, filename_dme, data_folder,
                                                                        nb_words[:len(codebook_list)], codebook_list, c)
                                        for idx_test, (pat_test_norm, pat_test_dme) 
                                        in enumerate(zip(filename_normal, filename_dme)))

        result_config.append(results_cv)

    # We have to store the final results
    output_folder = sys.argv[3]
    path_to_save = join(output_folder, 'r_' + str(radius) + '_' + codebook_type)
    if not os.path.exists(path_to_save):
        os.makedirs(path_to_save)

    from sklearn.externals import joblib
    joblib.dump(result_config, join(path_to_save, 'bow.pkl'))
