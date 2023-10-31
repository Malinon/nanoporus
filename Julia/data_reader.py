import julia
import numpy as np

LAMMPS_HEADER_ATOMS = "Atoms"

def write_entry(input_line, grid_step, output_grid):
    nums_str = input_line.split(" ")
    x = int(float(nums_str[2]) / grid_step)
    y = int(float(nums_str[3]) / grid_step)
    z = int(float(nums_str[4]) /  grid_step)
    output_grid[x, y, z] = True

def read_material_from_file(path, grid_size=200, grid_step=2.023):
    input_file = open(path, 'r')
    lines = input_file.readlines()
    line_idx = 0
    while not LAMMPS_HEADER_ATOMS in lines[line_idx]:
        line_idx += 1
    line_idx += 2
    output_grid = np.full((grid_size, grid_size, grid_size), False)
    while line_idx < len(lines):
        write_entry(lines[line_idx], grid_step, output_grid)
        line_idx += 1
    
    return output_grid



