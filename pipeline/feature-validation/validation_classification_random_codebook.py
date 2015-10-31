import numpy as np
import seaborn as sns
sns.set(color_codes=True)
import matplotlib.pyplot as plt
from sklearn.externals import joblib


print ''
print 'LBP riu + local mapping + flatten'
print ''

nw = [10, 20, 30, 40, 50, 60, 70, 80, 90,
      100, 200, 300, 400, 500,
      1000]

def report_plot(path):

    # Three subplots sharing both x/y axes
    f, (ax1, ax2, ax3) = plt.subplots(3, sharex=True, sharey=True)

    for radius in range(1, 4):

        path_result = path + '/r_' + str(radius) + '_bow/bow.pkl'

        print '----- # RADIUS {} -----'.format(radius)

        # Load the results from the given path
        result = joblib.load(path_result)
        result_array = np.array(result)

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

        #color_map = dict(slow="indianred", average="darkseagreen", fast="steelblue")
        # sns.tsplot(specificity_word, color="indianred", condition="Specificity")
        # sns.tsplot(sensitivity_word, color="darkseagreen", condition="Sensitivity")
        # sns.tsplot(accuracy_word, color="steelblue", condition="Accuracy")
        # sns.tsplot(specificity_word, time=np.array(nw), color="indianred", condition="Specificity")
        # sns.tsplot(sensitivity_word, time=np.array(nw), color="darkseagreen", condition="Sensitivity")
        #sns.tsplot(f1_word, time=np.array(nw), condition="F1 Score - Radius " + str(radius))
        #sns.tsplot(accuracy_word, time=np.array(nw), condition="Accuracy - Radius " + str(radius))

        if (radius == 1):
            ax1.plot(np.array(nw), accuracy_word, label='Accuracy - Radius ' + str(radius))
            ax1.plot(np.array(nw), f1_word, label='F1 score - Radius ' + str(radius))
            ax1.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
        elif (radius == 2):
            ax2.plot(np.array(nw), accuracy_word, label='Accuracy - Radius ' + str(radius))
            ax2.plot(np.array(nw), f1_word, label='F1 score - Radius ' + str(radius))
            ax2.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
        elif (radius == 3):
            ax3.plot(np.array(nw), accuracy_word, label='Accuracy - Radius ' + str(radius))
            ax3.plot(np.array(nw), f1_word, label='F1 score - Radius ' + str(radius))
            ax3.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
            
        # Fine-tune figure; make subplots close to each other and hide x ticks for
        # all but bottom plot.
        f.subplots_adjust(hspace=.2)
        #plt.setp([a.get_xticklabels() for a in f.axes[:-1]], visible=False)

        #plt.plot(np.array(nw), accuracy_word, label='Accuracy - Radius ' + str(radius))
        #plt.plot(np.array(nw), f1_word, label='F1 score - Radius ' + str(radius))

    plt.xlabel('Number of words')
    plt.show()


# # Define the path for flatten image
# path_result = '/data/retinopathy/OCT/SERI/results/flatten/lbp_riu/lbp_global'

# report_plot(path_result)

# Define the path for flatte and aligned image 
path_result = '/data/retinopathy/OCT/SERI/results/flatten_aligned/lbp_riu/lbp_global'

report_plot(path_result)
