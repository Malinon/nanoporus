"""
This script generates and saves persistence intervals of dim 0,1,2 based on filtration
"""
print("PreStart")

import numpy as np
import joblib
import gudhi as gd
import gudhi.representations
import numpy as np
import sys
import zipfile

print("Start")
HEIGHT = sys.argv[1]
RADIUS = HEIGHT * sys.argv[2]
IS_TOPO = sys.argv[2]

SAMPLE_NUM = 110 if IS_TOPO else 75


NAME = "cone_{radius}_{height}".format(radius = RADIUS, height= HEIGHT)
DIR_NAME = "filtrations/" +NAME + ("/topo" if IS_TOPO else "/rand")
OUT_NAME = "persistence_" + NAME + ("_topo" if IS_TOPO else "_rand")

def gen_in_name(i):
    return DIR_NAME + "/filtration_{i}".format(i=i)


def read_filtration(file_name):
    with open(file_name, 'r') as fp:
        nums = [float(l) for l in fp.readlines()]
        size = int((len(nums)) ** (1.0 / 3))
        out_array = np.empty((size, size, size))
        count=0
        for z in range(size):
            for y in range(size):
                for x in range(size):
                    out_array[x,y,z] = nums[count]
                    count += 1
        return out_array

def get_persisistence_from_filtration_file(file_name):
    filtr = read_filtration(file_name)
    comp = gd.PeriodicCubicalComplex(top_dimensional_cells=filtr, periodic_dimensions=[False, False, True])
    comp.compute_persistence()
    return [comp.persistence_intervals_in_dimension(i) for i in range(3)]

dgms = [[],[],[]]
print("Start real")
#with zipfile.ZipFile('filtrations/' + NAME + ".zip") as myzip:
#    myzip.extractall()
for i in range(SAMPLE_NUM):
    print("case ", i)
    file_name = gen_in_name(i)
    pers = get_persisistence_from_filtration_file(file_name)
    for j in range(3):
        dgms[j].append(pers[j])

joblib.dump(dgms, OUT_NAME)