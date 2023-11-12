from multiprocessing import Pool
import data_reader as dr
import numpy as np
import joblib
import gudhi as gd

from julia.api import Julia


INPUT_DIRECTORY = "../results_topo/"#"../simulation_results/"
OUTPUT_TMPL = "cub_complex_topo_"



def save_complex(i):
    jl = Julia(compiled_modules=False)
    from julia import Main
    Main.include("filtrator.jl")
    #input_path = INPUT_DIRECTORY  + str(i) + ".lpm"
    input_path = INPUT_DIRECTORY  + "lmp_data_topo_" + str(i)
    data = dr.read_material_from_file(input_path)
    # filtr = gd.CubicalComplex(top_dimensional_cells=Main.calculate_zcone_filtration(data))
    output_file = OUTPUT_TMPL + str(i)
    joblib.dump(Main.calculate_zcone_filtration(data), output_file)
    print("Done ", i)

if __name__ == '__main__':
    with Pool(processes=5) as p:
        p.map(save_complex, range(6,8))
