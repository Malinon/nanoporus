
def __is_in_range(x, y, z, data):

    return 0 <= x and x < data.shape[0] and 0 <= y and y < data.shape[1] and 0 <= z and z < data.shape[2]


def get_weighted_pyramide_filtration(point, data, z_multiplier = 0.5, xy_multiplier = 0.5, range_filt=5):
    filtration_value = 0.0
    entries_weight = 0
    for z in range(-range_filt, range_filt + 1):
        z_abs = abs(z)
        z_idx = point[2] + z
        for x in range(-z_abs, z_abs  + 1):
            x_idx = point[0] + x
            x_abs = abs(x)
            for y in range(-z_abs, z_abs + 1):
                y_idx = point[1] + y
                if __is_in_range(x_idx, y_idx, z_idx, data):
                    weight = (z_multiplier ** z_abs) * (xy_multiplier ** (x_abs + abs(y)))
                    entries_weight += weight
                    if data[x_idx, y_idx, z_idx]:
                        filtration_value += weight
    return filtration_value / entries_weight
                    

    