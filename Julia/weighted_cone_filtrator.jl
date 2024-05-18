struct WeightedConeFiltratorZ
    height::Float64
    radius::Float64
    max_X::Int64
    max_Y::Int64
    max_Z::Int64
    normalized_vector::Tuple{Float64, Float64, Float64}
    function WeightedConeFiltratorZ(radius::Float64, vector::Tuple{Float64, Float64, Float64})
        h = sqrt(vector[1]^2 + vector[2]^2 + vector[3]^2)
        new(h, radius, ceil(radius), ceil(radius), abs(ceil(vector[3])), (vector[1] / h, vector[2] / h, vector[3] /h ))
    end
end

"""
    get_weighted_impact(cFiltrator::WeightedConeFiltratorZ, x, y, z, x_tip, y_tip, z_tip, height_multiplier, radius_multiplier)

Calculates the weighted impact of a point on a weighted cone filtrator.

# Arguments
- `cFiltrator::WeightedConeFiltratorZ`: The weighted cone filtrator object.
- `x, y, z`: The coordinates of the point.
- `x_tip, y_tip, z_tip`: The coordinates of the tip of the cone.
- `height_multiplier`: The height multiplier.
- `radius_multiplier`: The radius multiplier.

# Returns
- If the point is within the cone, it returns the weighted impact value.
- If the point is outside the cone, it returns `0`.
"""
function get_weighted_impact(cFiltrator::WeightedConeFiltratorZ, x, y, z, x_tip, y_tip, z_tip, height_multiplier, radius_multiplier)
    x_diff = x_tip - x
    y_diff = y_tip - y
    z_diff = z_tip - z
    cone_dist = x_diff * cFiltrator.normalized_vector[1] + y_diff * cFiltrator.normalized_vector[2] + z_diff * cFiltrator.normalized_vector[3]
    if cone_dist > cFiltrator.height || cone_dist < -cFiltrator.height
        return false
    end
    orth_distance = sqrt((x_diff - cone_dist * cFiltrator.normalized_vector[1])^2 +
        (y_diff - cone_dist * cFiltrator.normalized_vector[2])^2 + (z_diff - cone_dist * cFiltrator.normalized_vector[3])^2)
    cone_radius = cFiltrator.radius * abs(cone_dist) / cFiltrator.height
    if orth_distance <= cone_radius
        return (radius_multiplier^orth_distance) * (height_multiplier^abs(cone_dist))
    else
        return 0
    end
end

function call(cFiltrator::WeightedConeFiltratorZ, x, y, z, input_grid::Array{Bool}, radius_multiplier, height_multiplier)
    weights_full_sum = 0.0
    weights_empty_sum = 0.0
    GRID_SHAPE = size(input_grid)
    START_J = max(1, y-cFiltrator.max_Y)
    STOP_J = min(y + cFiltrator.max_Y, GRID_SHAPE[2])
    START_K = max(1, z-cFiltrator.max_Z)
    STOP_K = min(z + cFiltrator.max_Z, GRID_SHAPE[3])
    for i in max(1, x-cFiltrator.max_X):min(x + cFiltrator.max_X, GRID_SHAPE[1])
        for j in START_J:STOP_J
            for k in START_K:STOP_K
                weight = get_weighted_impact(cFiltrator, i, j, k, x, y, z, height_multiplier, radius_multiplier)
                if input_grid[i, j, k]
                    weights_full_sum += weight
                else
                    weights_empty_sum += weight
                end
            end
        end
    end
    return weights_full_sum / (weights_full_sum + weights_empty_sum)
end