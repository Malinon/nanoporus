include("../../weighted_cone_filtrator.jl")
using Test

const grid_length = 20

@testset begin
@testset "Empty datsets gives zeroes" begin
    empty_sample = fill(false, (grid_length, grid_length, grid_length))
    filtrator =  WeightedConeFiltratorZ(3.0, (0.0, 0.0, 7.0))
    for i in 1:grid_length
        for j in 1:grid_length
            for k in 1:grid_length
                @test 0.0 == call(filtrator, i, j, k, empty_sample, 0.5, 0.75)
            end
        end
    end
end

@testset "Full datsets gives ones" begin
    full_sample = fill(true, (grid_length, grid_length, grid_length))
    filtrator =  WeightedConeFiltratorZ(3.0, (0.0, 0.0, 7.0))
    for i in 1:grid_length
        for j in 1:grid_length
            for k in 1:grid_length
                @test 1 == call(filtrator, i, j, k, full_sample, 2, 2)
            end
        end
    end
end

@testset "Empty cone gives zeroes" begin
    filtrator =  WeightedConeFiltratorZ(1.0, (0.0, 0.0, 2.0))
    sample = fill(true, (grid_length, grid_length, grid_length))
    sample[5,5,5] = false

    sample[5,5,4] = false
    sample[5,5,3] = false

    sample[5,4,3] = false
    sample[5,6,3] = false
    sample[4,5,3] = false
    sample[6,5,3] = false

    sample[5,5,6] = false
    sample[5,5,7] = false

    sample[5,6,7] = false
    sample[5,4,7] = false
    sample[6,5,7] = false
    sample[4,5,7] = false
    @test 0 == call(filtrator, 5, 5, 5, sample, 1, 1)
end

@testset "Full cone gives one" begin
    filtrator =  WeightedConeFiltratorZ(1.0, (0.0, 0.0, 2.0))
    sample = fill(false, (grid_length, grid_length, grid_length))
    sample[5,5,5] = true

    sample[5,5,4] = true
    sample[5,5,3] = true

    sample[5,4,3] = true
    sample[5,6,3] = true
    sample[4,5,3] = true
    sample[6,5,3] = true

    sample[5,5,6] = true
    sample[5,5,7] = true

    sample[5,6,7] = true
    sample[5,4,7] = true
    sample[6,5,7] = true
    sample[4,5,7] = true
    @test 1 == call(filtrator, 5, 5, 5, sample, 1, 1)
end

@testset "Full cells are detected" begin
    sample = fill(false, (grid_length, grid_length, grid_length))
    filtrator =  WeightedConeFiltratorZ(1.0, (0.0, 0.0, 2.0))
    sample[5,5,5] = true
    sample[5,5,6] = true
    sample[5,6,3] = true
    for height_multiplier in 1:3
        for radius_multiplier in 1:3
            sum_of_weights = (height_multiplier + height_multiplier^2 +  radius_multiplier * (height_multiplier^2) * 4) * 2 + 1
            @test  (((1 + height_multiplier+ radius_multiplier * (height_multiplier^2)) / sum_of_weights) == call(
                    filtrator, 5, 5, 5, sample, radius_multiplier, height_multiplier))
        end
    end
end
end