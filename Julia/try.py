from multiprocessing import Pool
import data_reader as dr
import numpy as np
import joblib
import gudhi as gd

from julia.api import Julia


jl = Julia(compiled_modules=False)
from julia import Main
Main.include("filtrator.jl")
input_path = "../simulation_results/lmp_data_3"
data = dr.read_material_from_file(input_path)
    # filtr = gd.CubicalComplex(top_dimensional_cells=Main.calculate_zcone_filtration(data))
a = Main.calculate_zcone_filtration(data)
print(type(a))
counter = 0
for i in range(200):
     for j in range(200):
         for k in range(200):
             if not a[i, j, k] == 0:
                counter = counter + 1   
print(counter)
counter = 0
for i in range(200):
     for j in range(200):
         for k in range(200):
             if not data[i, j, k] == 0:
                counter = counter + 1
print(counter)