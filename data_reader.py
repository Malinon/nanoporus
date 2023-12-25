import julia
import numpy as np

LAMMPS_HEADER_ATOMS = "Atoms"
MAX_X_TAG = "xhi"

def write_entry(input_line, grid_step, output_grid):
    nums_str = input_line.split(" ")
    x = int(float(nums_str[2]) / grid_step)
    y = int(float(nums_str[3]) / grid_step)
    z = int(float(nums_str[4]) /  grid_step)
    output_grid[x, y, z] = True

def get_max_x_from_line(input_line, grid_step):
    parts = input_line.split(" ")
    return round(float(parts[1]) / grid_step)

def read_material_from_file(path, grid_step=2.023, i=0):
    input_file = open(path, 'r')
    lines = input_file.readlines()
    line_idx = 0
    while not MAX_X_TAG in lines[line_idx]:
        line_idx += 1
    grid_size = get_max_x_from_line(lines[line_idx], grid_step)
    if grid_size > 250:
        print(i)
    while not LAMMPS_HEADER_ATOMS in lines[line_idx]:
        line_idx += 1
    line_idx += 2
    output_grid = np.full((grid_size, grid_size, grid_size), False)
    while line_idx < len(lines):
        write_entry(lines[line_idx], grid_step, output_grid)
        line_idx += 1
    
    return output_grid



