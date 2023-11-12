Module

include("cone_filtrator.jl")

function calculate_filtration(input_grid, filtrator)
    GRID_SHAPE = size(input_grid)
    max_dim_cell_filtration_values = zeros(GRID_SHAPE[1], GRID_SHAPE[2], GRID_SHAPE[3])
    # Sequnential
    for i in 1:GRID_SHAPE[1]
        for j in 1:GRID_SHAPE[2]
            for k in 1:GRID_SHAPE[3]
                # print("Next ", [i, j, k])
                max_dim_cell_filtration_values[i, j, k] = call(filtrator, i, j, k, input_grid)
            end
        end
    end
    return max_dim_cell_filtration_values
end

function calculate_zcone_filtration(input_grid)
    filtrator = ConFiltratorZ(10.0, (0.0, 0.0, 20.0))
    return calculate_filtration(input_grid, filtrator)
end

function test(x)
    print(x + 1)
end



