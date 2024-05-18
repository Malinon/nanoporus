"""
    struct ConFiltratorZ

A struct representing a cone-shaped filtrator in 3D space.

# Fields
- `height::Float64`: The height of the cone.
- `radius::Float64`: The radius of the cone.
- `max_X::Int64`: The maximum X-coordinate value.
- `max_Y::Int64`: The maximum Y-coordinate value.
- `max_Z::Int64`: The maximum Z-coordinate value.
- `normalized_vector::Tuple{Float64, Float64, Float64}`: The normalized vector representing the direction of the cone.

# Constructors
- `ConFiltratorZ(radius::Float64, vector::Tuple{Float64, Float64, Float64})`: Constructs a `ConFiltratorZ` object with the given radius and vector.

"""
struct ConFiltratorZ
    height::Float64
    radius::Float64
    max_X::Int64
    max_Y::Int64
    max_Z::Int64
    normalized_vector::Tuple{Float64, Float64, Float64}
    function ConFiltratorZ(radius::Float64, vector::Tuple{Float64, Float64, Float64})
        h = sqrt(vector[1]^2 + vector[2]^2 + vector[3]^2)
        new(h, radius, ceil(radius), ceil(radius), abs(ceil(vector[3])), (vector[1] / h, vector[2] / h, vector[3] /h ))
    end
end

"""
    isPointInCones(cFiltrator::ConFiltratorZ, x, y, z, x_tip, y_tip, z_tip)

Check if a point is inside the cones defined by a cone filtrator.

# Arguments
- `cFiltrator::ConFiltratorZ`: The cone filtrator object.
- `x, y, z`: The coordinates of the point.
- `x_tip, y_tip, z_tip`: The coordinates of the tip of the cone.

# Returns
- `true` if the point is inside the cones, `false` otherwise.
"""
function isPointInCones(cFiltrator::ConFiltratorZ, x, y, z, x_tip, y_tip, z_tip)
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
    return orth_distance <= cone_radius
end

"""
    call(cFiltrator::ConFiltratorZ, x, y, z, input_grid::Array{Bool})

Compute the ratio of points inside cones to the total number of points in a given region.

# Arguments
- `cFiltrator::ConFiltratorZ`: The cone filtrator object.
- `x`: The x-coordinate of the center point.
- `y`: The y-coordinate of the center point.
- `z`: The z-coordinate of the center point.
- `input_grid::Array{Bool}`: The input grid containing boolean values indicating whether a point is occupied or not.

# Returns
The ratio of points inside cones to the total number of points in the region.

"""
function call(cFiltrator::ConFiltratorZ, x, y, z, input_grid::Array{Bool})
    # function body
end
function call(cFiltrator::ConFiltratorZ, x, y, z, input_grid::Array{Bool})
    inside_cones_empty = 0.0
    inside_cones_full = 0.0
    GRID_SHAPE = size(input_grid)
    START_J = max(1, y-cFiltrator.max_Y)
    STOP_J = min(y + cFiltrator.max_Y, GRID_SHAPE[2])
    START_K = max(1, z-cFiltrator.max_Z)
    STOP_K = min(z + cFiltrator.max_Z, GRID_SHAPE[3])
    for i in max(1, x-cFiltrator.max_X):min(x + cFiltrator.max_X, GRID_SHAPE[1])
        for j in START_J:STOP_J
            for k in START_K:STOP_K
                if isPointInCones(cFiltrator, i, j, k, x, y, z)
                    if input_grid[i, j, k]
                        inside_cones_full += 1.0
                    else
                        inside_cones_empty += 1.0
                    end
                end
            end
        end
    end
    return inside_cones_full / (inside_cones_empty + inside_cones_full)
end
