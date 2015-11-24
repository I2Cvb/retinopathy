import numpy as np
import seaborn as sns
sns.set(color_codes=True)
import matplotlib.pyplot as plt
from sklearn.externals import joblib
import matplotlib

# font = {'family' : 'normal',
#         'weight' : 'bold',
#         'size'   : 40}

# matplotlib.rc('font', **font)

# matplotlib.rcParams.update({'font.size': 200})

counter_fig = 1

def report_plot(path, nw, config, title):

    # Three subplots sharing both x/y axes
    f, (ax1, ax2) = plt.subplots(1, 2)

    mylines = []
    for radius in range(1, 4):

        path_result = path + '/r_' + str(radius) + '_codebook_random/bow.pkl'

        print '----- # RADIUS {} -----'.format(radius)

        # Load the results from the given path
        result_all_config = joblib.load(path_result)

        # Get only the logistic regression configuration
        result_all_config = [result_all_config[4]]


        for result in result_all_config:
            
            result_array = np.array(result)
            print result_array.shape

            # Swap the two first axis
            result_array = np.rollaxis(result_array, 0, 2)

            ###############################################
            #### TMP SHOULD BE REMOVED AT SOME POINT ######
            result_array = result_array[:len(nw), :, :]
            print result_array.shape


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

            line, = ax2.semilogx(np.array(nw), f1_word, label='Radius ' + str(radius))
            ax2.set_xlabel('Number of words', fontsize=14)
            ax2.set_ylabel('F1 score', fontsize=14)
            ax2.set_ylim(0., 1.)
            ax2.tick_params(axis='x', labelsize=11)
            ax2.tick_params(axis='y', labelsize=11)
            ax2.set_xticks([10, 20, 30, 40, 50, 60, 70, 80, 90,
                            100, 200, 300, 400, 500, 600, 700, 800, 900,
                            1000, 2000, 3000, 4000, 5000])
            ax2.set_xlim(10, nw[-1])
            # ax2.set_xticklabels(['10', '', '', '', '', '', '', '', '',
            #                      '100', '', '', '', '', '', '', '', '',
            #                      '1000'])
            #ax2.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
            # ax2.semilogx(np.array(nw), f1_word, label='F1 score - Radius ' + str(radius))
            # ax2.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
            # ax2.semilogx(np.array(nw), f1_word, label='F1 score - Radius ' + str(radius))

            mylines.append(line)

            ax1.semilogx(np.array(nw), accuracy_word, label='Radius ' + str(radius))
            ax1.set_xlabel('Number of words', fontsize=14)
            ax1.set_ylabel('Accuracy', fontsize=14)
            ax1.set_ylim(0., 1.)
            ax1.tick_params(axis='x', labelsize=11)
            ax1.tick_params(axis='y', labelsize=11)
            ax1.set_xticks([10, 20, 30, 40, 50, 60, 70, 80, 90,
                            100, 200, 300, 400, 500, 600, 700, 800, 900,
                            1000, 2000, 3000, 4000, 5000])
            ax1.set_xlim(10, nw[-1])
            # ax1.semilogx(np.array(nw), accuracy_word, label='Accuracy - Radius ' + str(radius))
            # ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
            # ax1.semilogx(np.array(nw), accuracy_word, label='Accuracy - Radius ' + str(radius))
            # ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)

            # Fine-tune figure; make subplots close to each other and hide x ticks for
            # all but bottom plot.
            #f.subplots_adjust(hspace=.1)

    plt.figlegend(mylines, ('Radius 1', 'Radius 2', 'Radius 3'), 
                  fontsize=14, loc='upper center', ncol=5, bbox_to_anchor=(.45, 1.))
    lgd = plt.suptitle(title, fontsize=14, y=1.04)
    # plt.show()
    global counter_fig
    filename = 'figure' + str(counter_fig) + '.pdf'
    f.savefig(filename, bbox_extra_artists=(lgd,), bbox_inches='tight')
    counter_fig += 1


config = [{'classifier_str' : 'random-forest', 'n_estimators' : 100, 'gs_n_jobs' : 8},
          {'classifier_str' : 'knn', 'n_neighbors' : 3, 'gs_n_jobs' : 8},
          {'classifier_str' : 'knn', 'n_neighbors' : 5, 'gs_n_jobs' : 8},
          {'classifier_str' : 'knn', 'n_neighbors' : 7, 'gs_n_jobs' : 8},
          {'classifier_str' : 'logistic-regression', 'gs_n_jobs' : 8},
          {'classifier_str' : 'kernel-svm', 'gs_n_jobs' : 8},
          {'classifier_str' : 'gradient-boosting', 'n_estimators' : 100, 'gs_n_jobs' : 8}]

# Check the following configuration:
# ##### LBP + BOW + LOCAL #####

nw = [10, 20, 30, 40, 50, 60, 70, 80, 90,
      100, 200, 300, 400, 500,
      1000, 2000, 3000, 4000, 5000]

# ### Non-flatten
# Define the path for non flatten image
path_result = '/data/retinopathy/OCT/SERI/results/non_flatten/lbp_riu/lbp_hist/lbp_local'

report_plot(path_result, nw, config, 'LBP + local + BoW + non-flatten')

### Flatten
# Define the path for flatten image
path_result = '/data/retinopathy/OCT/SERI/results/flatten/lbp_riu/lbp_hist/lbp_local'

report_plot(path_result, nw, config, 'LBP + local + BoW + flatten')

### Flatten-aligned
# Define the path for flatten image
path_result = '/data/retinopathy/OCT/SERI/results/flatten_aligned/lbp_riu/lbp_hist/lbp_local'

report_plot(path_result, nw, config, 'LBP + local + BoW + flatten-aligned')

### Flatten-aligned cropped
# Define the path for flatten image

nw = [10, 20, 30, 40, 50, 60, 70, 80, 90,
      100, 200, 300, 400, 500,
      1000]

path_result = '/data/retinopathy/OCT/SERI/results/flatten_aligned_cropped/lbp_riu/lbp_hist/lbp_local'

report_plot(path_result, nw, config, 'LBP + local + BoW + flatten-aligned-cropped')

# Check the following configuration:
##### LBP + BOW + GLOBAL #####

nw = [10, 20, 30, 40, 50, 60, 70, 80, 90,
      100, 200, 300, 400, 500,
      1000]

### Non-flatten
# Define the path for non flatten image
path_result = '/data/retinopathy/OCT/SERI/results/non_flatten/lbp_riu/lbp_hist/lbp_global'

report_plot(path_result, nw, config, 'LBP + global + BoW + non-flatten')

### Flatten
# Define the path for flatten image
path_result = '/data/retinopathy/OCT/SERI/results/flatten/lbp_riu/lbp_hist/lbp_global'

report_plot(path_result, nw, config, 'LBP + global + BoW + flatten')

### Flatten-aligned
# Define the path for flatten image
path_result = '/data/retinopathy/OCT/SERI/results/flatten_aligned/lbp_riu/lbp_hist/lbp_global'

report_plot(path_result, nw, config, 'LBP + global + BoW + flatten-aligned')

### Flatten-aligned cropped
# Define the path for flatten image
path_result = '/data/retinopathy/OCT/SERI/results/flatten_aligned_cropped/lbp_riu/lbp_hist/lbp_global'

report_plot(path_result, nw, config, 'LBP + global + BoW + flatten-aligned-cropped')

#Check the following configuration:
#### LBP-TOP + BOW + LOCAL #####

nw = [10, 20, 30, 40, 50, 60, 70, 80, 90,
      100, 200, 300, 400, 500,
      1000, 2000, 3000, 4000, 5000]

### Non-flatten
# Define the path for non flatten image
path_result = '/data/retinopathy/OCT/SERI/results/non_flatten/lbp_riu/lbp_hist_top/lbp_local'

report_plot(path_result, nw, config, 'LBP-TOP + local + BoW + non-flatten')

### Flatten
# Define the path for flatten image
path_result = '/data/retinopathy/OCT/SERI/results/flatten/lbp_riu/lbp_hist_top/lbp_local'

report_plot(path_result, nw, config, 'LBP-TOP + local + BoW + flatten')

### Flatten-aligned
# Define the path for flatten image
path_result = '/data/retinopathy/OCT/SERI/results/flatten_aligned/lbp_riu/lbp_hist_top/lbp_local'

report_plot(path_result, nw, config, 'LBP-TOP + local + BoW + flatten-aligned')

# ### Flatten-aligned cropped
# Define the path for flatten image
path_result = '/data/retinopathy/OCT/SERI/results/flatten_aligned_cropped/lbp_riu/lbp_hist_top/lbp_local'

report_plot(path_result, nw, config, 'LBP-TOP + local + BoW + flatten-aligned-cropped')
