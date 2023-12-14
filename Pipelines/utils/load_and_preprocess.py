import joblib
import numpy as np
import gudhi as gd
import gudhi.representations

from splitted_data import SplitedData
from consts import *

class Transformer:
    def __init__(self):
        self.persistence_imagers = [gd.representations.PersistenceImage(resolution=PERSISTENCE_IMAGE_RESOLUTION) for i in range(3)]
    def fit(self, X, Y=None):
        for i in range(len(self.persistence_imagers)):
            self.persistence_imagers[i].fit(X[i])
    def transform(self, X):
        transformed_X  = []
        for i in range(len(X[0])):
            transformed_X.append(np.concatenate(np.array([self.persistence_imagers[dim](X[dim][i]) for dim in range(3)])))
        return transformed_X

def load_labels(path, feature_name):
    f = open(path + feature_name + "_topo", "r")
    lines = f.readlines()
    labs_top = [float(lines[i]) for i in range(SAMPLES_PER_TYPE) if not i in EXCL_TOPO]
    f.close()
    
    f = open(path + feature_name + "_rand", "r")
    lines = f.readlines()
    labs_rand = [float(lines[i]) for i in range(SAMPLES_PER_TYPE)]
    f.close()
    return labs_top + labs_rand


def load_from_csv(path):
    return [np.loadtxt(str(i) + path, dtype=float, delimiter=",") for i in range(3)]

""" This function vectorise persistence intervals (perisistence image), split data and dump it"""
def prepare_data(filtration_params, data_file_name_generator, labels_path, output_name_generator):
    gudhi_diag_selector = gd.representations.DiagramSelector(use=True,limit=np.inf, point_type="finite")
    select = lambda x: ([ [ gudhi_diag_selector(x[i][j]) for j in range(len(x[i]))] for i in range(len(x)) ])
    dgms_topo = select(load_from_csv(data_file_name_generator(filtration_params, True)))
    dgms_rand = select(load_from_csv(data_file_name_generator(filtration_params, False)))
    data = np.transpose(load_from_csv((np.array(dgms_topo), np.array(dgms_rand)), axis=1))
    yield_labels = load_labels(labels_path, "yield")
    modulus_labels = load_labels(labels_path, "modulus")
    idxs_all = [i for i in range(len(yield_labels))]
    
    whole_data = SplitedData(data, yield_labels, modulus_labels, idxs_all, Transformer())
    topo_data = SplitedData(data, yield_labels, modulus_labels, [i for i in range(NUMBER_OF_OK_TOPO_SAMPLES)], Transformer())
    rand_data = SplitedData(data, yield_labels, modulus_labels,
            [i for i in range(NUMBER_OF_OK_TOPO_SAMPLES, NUMBER_OF_OK_TOPO_SAMPLES + SAMPLES_PER_TYPE)], Transformer())

    basic_output_name = output_name_generator(filtration_params)
    joblib.dump(whole_data, basic_output_name)
    joblib.dump(topo_data, basic_output_name + "_topo")
    joblib.dump(rand_data, basic_output_name + "_rand")