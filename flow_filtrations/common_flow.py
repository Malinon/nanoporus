SOURCE_NODE = 0
SINK_NODE = 1

def is_in_circle(radius_squared, center, x, y):
    return (x - center[0])**2 + (y - center[1])**2 <= radius_squared

def create_slice(radius, center, data_shape):
    MIN_Y = max(0, center[1] - radius)
    MAX_Y = min(data_shape[1] - 1, center[1] + radius)
    RADIUS_SQUARED = radius ** 2
    points_in_circle = []
    for x in range(max(0, center[0] - radius), min(data_shape[0] -1, center[0] + radius) + 1):
        for y in range(MIN_Y, MAX_Y + 1):
            if is_in_circle(RADIUS_SQUARED, center, x, y):
                points_in_circle.append((x,y))
    return points_in_circle
