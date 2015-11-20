import numpy as np
import seaborn as sns
sns.set(color_codes=True)
import matplotlib.pyplot as plt
from sklearn.externals import joblib

def report_plot(path, nw, config):

    # Three subplots sharing both x/y axes
    f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)

    for radius in range(1, 4):

        path_result = path + '/r_' + str(radius) + '_codebook_random/bow.pkl'

        print '----- # RADIUS {} -----'.format(radius)

        # Load the results from the given path
        result_all_config = joblib.load(path_result)

        for result in result_all_config:
            
            result_array = np.array(result)
            print result_array.shape

            # Swap the two first axis
            result_array = np.rollaxis(result_array, 0, 2)

            # Go throught the different words
            specificity_word = []
            sensitivity_word = []
            accuracy_word = []
            f1_word = []
            for idx_w, w in enumerate(result_array):

                normal = 0.
                dme = 0.
                # Extract the results on the testing set
                for cv in w[:, 0]:

                    if cv[0] == 0:
                        normal += 1.
                    if cv[1] == 1:
                        dme += 1.

                # Append the results for this word
                specificity_word.append(normal / float(result_array.shape[1]))
                sensitivity_word.append(dme / float(result_array.shape[1]))
                f1_word.append((2. * dme) / 
                               ((2. * dme) + 
                                (float(result_array.shape[1]) - normal) + 
                                (float(result_array.shape[1]) - dme)))
                accuracy_word.append((normal + dme) / float(result_array.shape[1] * 2.))

                print '----- # WORDS {} -----'.format(nw[idx_w])
                print 'The statistic are the following:'
                print 'Sensitivity: {} - Specificity: {}'.format(dme / float(result_array.shape[1]),
                                                                 normal / float(result_array.shape[1]))
                print 'DME: {} / {} - Normal: {}/ {}'.format(dme,
                                                             float(result_array.shape[1]),
                                                             normal,
                                                             float(result_array.shape[1]))
                print ''

            if (radius == 1):
                ax1.semilogx(np.array(nw), f1_word, label='F1 score - Radius ' + str(radius))
                ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
            elif (radius == 2):
                ax2.semilogx(np.array(nw), f1_word, label='F1 score - Radius ' + str(radius))
                ax2.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
            elif (radius == 3):
                ax3.semilogx(np.array(nw), f1_word, label='F1 score - Radius ' + str(radius))
                ax3.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)

            # Fine-tune figure; make subplots close to each other and hide x ticks for
            # all but bottom plot.
            f.subplots_adjust(hspace=.2)

        plt.xlabel('Number of words')
        plt.show()

    # Three subplots sharing both x/y axes
    f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)

    for radius in range(1, 4):

        path_result = path + '/r_' + str(radius) + '_codebook_random/bow.pkl'

        print '----- # RADIUS {} -----'.format(radius)

        # Load the results from the given path
        result_all_config = joblib.load(path_result)

        for result in result_all_config:
            
            result_array = np.array(result)
            print result_array.shape

            # Swap the two first axis
            result_array = np.rollaxis(result_array, 0, 2)

            # Go throught the different words
            specificity_word = []
            sensitivity_word = []
            accuracy_word = []
            f1_word = []
            for idx_w, w in enumerate(result_array):

                normal = 0.
                dme = 0.
                # Extract the results on the testing set
                for cv in w[:, 0]:

                    if cv[0] == 0:
                        normal += 1.
                    if cv[1] == 1:
                        dme += 1.

                # Append the results for this word
                specificity_word.append(normal / float(result_array.shape[1]))
                sensitivity_word.append(dme / float(result_array.shape[1]))
                f1_word.append((2. * dme) / 
                               ((2. * dme) + 
                                (float(result_array.shape[1]) - normal) + 
                                (float(result_array.shape[1]) - dme)))
                accuracy_word.append((normal + dme) / float(result_array.shape[1] * 2.))

                print '----- # WORDS {} -----'.format(nw[idx_w])
                print 'The statistic are the following:'
                print 'Sensitivity: {} - Specificity: {}'.format(dme / float(result_array.shape[1]),
                                                                 normal / float(result_array.shape[1]))
                print 'DME: {} / {} - Normal: {}/ {}'.format(dme,
                                                             float(result_array.shape[1]),
                                                             normal,
                                                             float(result_array.shape[1]))
                print ''

            if (radius == 1):
                ax1.semilogx(np.array(nw), accuracy_word, label='Accuracy - Radius ' + str(radius))
                ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
            elif (radius == 2):
                ax2.semilogx(np.array(nw), accuracy_word, label='Accuracy - Radius ' + str(radius))
                ax2.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
            elif (radius == 3):
                ax3.semilogx(np.array(nw), accuracy_word, label='Accuracy - Radius ' + str(radius))
                ax3.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)

            # Fine-tune figure; make subplots close to each other and hide x ticks for
            # all but bottom plot.
            f.subplots_adjust(hspace=.2)

        plt.xlabel('Number of words')
        plt.show()


config = [{'classifier_str' : 'random-forest', 'n_estimators' : 100, 'gs_n_jobs' : 8},
          {'classifier_str' : 'knn', 'n_neighbors' : 3, 'gs_n_jobs' : 8},
          {'classifier_str' : 'knn', 'n_neighbors' : 5, 'gs_n_jobs' : 8},
          {'classifier_str' : 'knn', 'n_neighbors' : 7, 'gs_n_jobs' : 8},
          {'classifier_str' : 'logistic-regression', 'gs_n_jobs' : 8},
          {'classifier_str' : 'kernel-svm', 'gs_n_jobs' : 8},
          {'classifier_str' : 'gradient-boosting', 'n_estimators' : 100, 'gs_n_jobs' : 8}]

nw = [10, 20, 30, 40, 50, 60, 70, 80, 90,
      100, 200, 300, 400, 500,
      1000, 2000, 3000, 4000, 5000]

# Define the path for flatten image
path_result = '/data/retinopathy/OCT/SERI/results/flatten/lbp_riu/lbp_hist/lbp_local'

report_plot(path_result, nw, config)

# nw = [10, 20, 30, 40, 50, 60, 70, 80, 90,
#       100, 200, 300, 400, 500]

# # Define the path for flatten image
# path_result = '/work/le2i/gu5306le/retinopathy/OCT/Duke/results/flatten_aligned/lbp_riu/lbp_local'

# report_plot(path_result, nw, config)

# nw = [10, 20, 30, 40, 50, 60, 70, 80, 90,
#       100, 200, 300, 400, 500,
#       1000]

# # Define the path for flatten image
# path_result = '/data/retinopathy/OCT/SERI/results/flatten/lbp_riu/lbp_global'

# report_plot(path_result, nw, config)

# # Define the path for flatte and aligned image 
# path_result = '/data/retinopathy/OCT/SERI/results/flatten_aligned/lbp_riu/lbp_global'

# report_plot(path_result, nw, config)

# nw = [10, 20, 30, 40, 50, 60, 70, 80, 90,
#       100, 200, 300, 400, 500,
#       1000, 2000, 3000, 4000, 5000]

# # Define the path for flatten image
# path_result = '/data/retinopathy/OCT/SERI/results/flatten/lbp_riu/lbp_local'

# report_plot(path_result, nw, config)

# # Define the path for flatte and aligned image 
# path_result = '/data/retinopathy/OCT/SERI/results/flatten_aligned/lbp_riu/lbp_local'

# report_plot(path_result, nw, config)
