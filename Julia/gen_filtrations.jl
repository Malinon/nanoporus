#include("weighted.jl")
include("Julia/cone_filtrator/parser.jl")
include("parser.jl")

using DelimitedFiles

function gen_out_name(i, radius, height, is_topo)
    if is_topo
        return ("filtrations/cone_" * string(radius) * "_" * string(height) * "/topo/filtration_" * string(i))
    else
        return ("filtrations/cone_" * string(radius) * "_" * string(height) * "/rand/filtration_" * string(i))
    end
end

HEIGHT = parse(Float64, ARGS[1])
RADIUS = HEIGHT * parse(Float64, ARGS[2])
FILTRATOR = WeightedConeFiltratorZ(RADIUS, (0.0, 0.0, HEIGHT))
function filtrator(point, input_grid)
    return call(FILTRATOR, point[1], point[2], point[3], input_grid)
end



const IS_TOPO = parse(Bool, ARGS[3])
sample_num = IS_TOPO ? 110 : 75


function gen_filtration(i, filtrator)
    println("Case " * string(i))
    in_name = IS_TOPO ? ("../topo_results/" * string(i) * ".lmp") :  ("../simulation_results/lmp_data_" * string(i))
    dt = read_material_from_file(in_name)
    sh = size(dt, 1)
    out = zeros(sh, sh, sh)

    for x in 1:sh
        for y in 1:sh
            for z in 1:sh
                out[x, y, z] = filtrator((x, y, z), dt)
            end
        end
    end

    writedlm(gen_out_name(i, z_multiplier, xy_multiplier, range), out)
end


for i in 0:(sample_num - 1)
    gen_filtration(i, filtrator)
end
