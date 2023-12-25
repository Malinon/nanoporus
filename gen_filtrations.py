from weighted_filtration import get_weighted_pyramide_filtration
from data_reader import read_material_from_file
import joblib
from multiprocessing import Pool
import numpy as np

SAMPLE_NUM = 75
INPUT_NAME_TMPL = "../simulation_results/lmp_data_"
Z_MULTIPLIER = 0.5
XY_MULTIPLIER = 0.25
RANGE = 5
OUTPUT_NAME_TMPL = "filtration/rand/pyramide_" + str(Z_MULTIPLIER) + "_" +str(XY_MULTIPLIER) + "_" + str(RANGE) + "/filtration_"

def get_filtration(i):
    print(i)
    mat_data = read_material_from_file(INPUT_NAME_TMPL + str(i))
    filtration = np.empty(shape=mat_data.shape)
    for x in range(filtration.shape[0]):
        for y in range(filtration.shape[1]):
            for z in range(filtration.shape[2]):
                filtration[x, y, z] = get_weighted_pyramide_filtration((x, y, z), mat_data, z_multiplier = Z_MULTIPLIER,
                     xy_multiplier = XY_MULTIPLIER, range_filt=RANGE)
    joblib.dump(filtration, OUTPUT_NAME_TMPL + str(i))

with Pool(5) as p:
    p.map(get_filtration, list(range(SAMPLE_NUM)))

    