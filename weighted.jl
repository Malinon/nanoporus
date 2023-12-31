function __is_in_range(x, y, z, data)
    return 1 <= x && x <= size(data, 1) && 1 <= y && y <= size(data, 2) && 1 <= z && z <= size(data, 3)
end

function get_weighted_pyramide_filtration(point, data, z_multiplier = 0.5, xy_multiplier = 0.5, range_filt=5)
    filtration_value = 0.0
    entries_weight = 0
    for z in -range_filt:range_filt
        z_abs = abs(z)
        z_idx = point[3] + z
        for x in -z_abs:z_abs
            x_idx = point[1] + x
            x_abs = abs(x)
            for y in -z_abs:z_abs
                y_idx = point[2] + y
                if __is_in_range(x_idx, y_idx, z_idx, data)
                    weight = (z_multiplier ^ z_abs) * (xy_multiplier ^ (x_abs + abs(y)))
                    entries_weight += weight
                    if data[x_idx, y_idx, z_idx]
                        filtration_value += weight
                    end
                end
            end
        end
    end
    return filtration_value / entries_weight
end

