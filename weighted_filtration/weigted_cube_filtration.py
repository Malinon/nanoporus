def __is_in_range(x, y, z, data):
    return 0 <= x and x < data.shape[0] and 0 <= y and y < data.shape[1] and 0 <= z and z < data.shape[2]


def get_weighted_cube_filtration(point, data, z_multiplier = 0.5, xy_multiplier = 0.5, range_filt=5):
    """
    Calculates the weighted cube filtration value for a given point in a 3D data array.

    Parameters:
    - point (tuple): The coordinates of the point in the data array.
    - data (ndarray): The 3D data array.
    - z_multiplier (float): The multiplier for the z-axis weight. Default is 0.5.
    - xy_multiplier (float): The multiplier for the x and y-axis weight. Default is 0.5.
    - range_filt (int): The range of the cube filtration. Default is 5.

    Returns:
    - filtration_value (float): The calculated weighted cube filtration value.
    """
    filtration_value = 0.0
    entries_weight = 0
    for z in range(range_filt):
        z_idx = point[2] + z
        for x in range(range_filt):
            x_idx = point[0] + x
            for y in range(range_filt):
                y_idx = point[1] + y
                if __is_in_range(x_idx, y_idx, z_idx, data):
                    weight = (z_multiplier ** z) * (xy_multiplier ** (x + y))
                    entries_weight += weight
                    if data[x_idx, y_idx, z_idx]:
                        filtration_value += weight
    for z in range(1, range_filt):
        z_idx = point[2] - z
        for x in range(range_filt):
            x_idx = point[0] - x
            for y in range(range_filt):
                y_idx = point[1] - y
                if __is_in_range(x_idx, y_idx, z_idx, data):
                    weight = (z_multiplier ** z) * (xy_multiplier ** (x + y))
                    entries_weight += weight
                    if data[x_idx, y_idx, z_idx]:
                        filtration_value += weight
    return filtration_value / entries_weight
                    

    