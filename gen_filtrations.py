#from weighted_filtration import get_weighted_pyramide_filtration
from flow_filtrations.general_flow_filtration import gen_flow_filtration
from flow_filtrations.lattice_neighbour_graph import create_lattice_neighoubr_graph
from data_reader import read_material_from_file
import joblib
from multiprocessing import Pool
import numpy as np

SAMPLE_NUM = 75
INPUT_NAME_TMPL = "../simulation_results/lmp_data_"
RADIUS = 2
HEIGHT = 3
OUTPUT_NAME_TMPL = "filtrations/flow_r" + str(RADIUS) + "_h" +str(HEIGHT) + "/rand/filtration_"
print(OUTPUT_NAME_TMPL)

def get_filtration(i):
    print(i)
    mat_data = read_material_from_file(INPUT_NAME_TMPL + str(i))
    grapher = lambda point, data: create_lattice_neighoubr_graph(point, data, HEIGHT, RADIUS)
    filtration =  gen_flow_filtration(mat_data, grapher)
    joblib.dump(filtration, OUTPUT_NAME_TMPL + str(i))

with Pool(4) as p:
    p.map(get_filtration, list(range(SAMPLE_NUM)))

    