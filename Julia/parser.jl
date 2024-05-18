using LinearAlgebra

const LAMMPS_HEADER_ATOMS = "Atoms"
const MAX_X_TAG = "xhi"

function write_entry(input_line, grid_step, output_grid)
    nums_str = split(input_line, " ")
    x = Int(round(parse(Float64, nums_str[3]) / grid_step))
    y = Int(round(parse(Float64, nums_str[4]) / grid_step))
    z = Int(round(parse(Float64, nums_str[5]) / grid_step))
    output_grid[x + 1, y + 1, z + 1] = true
end

function get_max_x_from_line(input_line, grid_step)
    parts = split(input_line, " ")
    return Int(round(parse(Float64, parts[2]) / grid_step))
end

function read_material_from_file(path, grid_step=2.023, i=0)
    input_file = open(path, "r")
    lines = readlines(input_file)
    line_idx = 1
    while !(occursin(MAX_X_TAG, lines[line_idx]))
        line_idx += 1
    end
    grid_size = get_max_x_from_line(lines[line_idx], grid_step)
    if grid_size > 250
        println(i)
    end
    while !(occursin(LAMMPS_HEADER_ATOMS, lines[line_idx]))
        line_idx += 1
    end
    line_idx += 2
    output_grid = falses(grid_size, grid_size, grid_size)
    while line_idx <= length(lines)
        write_entry(lines[line_idx], grid_step, output_grid)
        line_idx += 1
    end
    return output_grid
end
