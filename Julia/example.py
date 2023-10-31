from multiprocessing import Pool
import data_reader as dr
import numpy as np
import joblib
import gudhi as gd

from julia.api import Julia



def save_complex(i):
    jl = Julia(compiled_modules=False)
    from julia import Main
    Main.include("filtrator.jl")
    input_path = "../simulation_results/lmp_data_" + str(i)
    data = dr.read_material_from_file(input_path)
    # filtr = gd.CubicalComplex(top_dimensional_cells=Main.calculate_zcone_filtration(data))
    output_file = "cub_complex_" + str(i)
    joblib.dump(Main.calculate_zcone_filtration(data), output_file)
    print("Done ", i)

if __name__ == '__main__':
    with Pool(processes=10) as p:
        p.map(save_complex, range(75))