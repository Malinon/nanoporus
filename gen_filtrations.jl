include("weighted.jl")
include("parser.jl")
using DelimitedFiles

function gen_out_name(i, z_multiplier, xy_multiplier, range)
    return ("filtrations/pyramide_" * string(z_multiplier) * "_" * string(xy_multiplier) * "_" * string(range) * "/rand/filtration_" * string(i))
end

function gen_filtration(i, z_multiplier, xy_multiplier, range)
    println("Case " * string(i))
    in_name = "../simulation_results/lmp_data_" * string(i)
    dt = read_material_from_file(in_name)
    sh = size(dt, 1)
    out = zeros(sh, sh, sh)

    for x in 1:sh
        for y in 1:sh
            for z in 1:sh
                out[x, y, z] = get_weighted_pyramide_filtration((x, y, z), dt)
            end
        end
    end

    writedlm(gen_out_name(i, z_multiplier, xy_multiplier, range), out)
end




for i in parse(Int64, ARGS[4]):74
    gen_filtration(i, parse(Float64, ARGS[1]), parse(Float64, ARGS[2]), parse(Int64, ARGS[3]))
end
