"""
This script generates and saves persistence intervals of dim 0,1,2 based on filtration
"""

import numpy as np
import joblib
import gudhi as gd
import gudhi.representations
from datetime import datetime
import sys


FILE_TMPL_IN = sys.argv[1]
FILE_NAME_OUT = sys.argv[2]
IS_TOPO = bool(sys.argv[3])
EXCLUDE_TOPO = []
if IS_TOPO:
    EXCLUDE_TOPO =  [15, 20, 21, 25, 26, 30, 35, 40, 45, 50, 65, 66, 70]

dgms = [[],[],[]]

def get_persisistence_from_filtration_file(file_name):
    filtr = joblib.load(file_name)
    comp = gd.CubicalComplex(top_dimensional_cells=filtr)
    now = datetime.now()
    print("Start ", now.strftime("%H:%M:%S"))
    comp.compute_persistence()
    print("Pers ", now.strftime("%H:%M:%S"))
    return [comp.persistence_intervals_in_dimension(i) for i in range(3)]


for i in range(75):
    if not i in EXCLUDE_TOPO:
        file_name = FILE_TMPL_IN + str(i)
        pers = get_persisistence_from_filtration_file(file_name)
        for j in range(3):
            dgms[j].append(pers[j])

joblib.dump(dgms, FILE_NAME_OUT)
