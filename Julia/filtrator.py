
import gudhi as gd
import numpy as np

def calculate_filtration(input_grid, filtration_at_point):
    max_dim_cell_filtration_values = np.ndarray(input_grid.shape)
    # Sequnential
    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            for k in range(input_grid.shape[2]):
                # print("Next ", [i, j, k])
                max_dim_cell_filtration_values[i, j, k] = filtration_at_point(i, j, k, input_grid)
    # TODO: Create multiprocessing version
    return gd.CubicalComplex(max_dim_cell_filtration_values)



