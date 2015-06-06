# todo: this is wrong but is serves the integration purpose
import numpy as np
def load_iris():
    from sklearn.datasets import load_iris
    d = load_iris()
    label = [1 if x else -1 for x in d.target==0 ]
    return (d.data, np.asarray(label))
