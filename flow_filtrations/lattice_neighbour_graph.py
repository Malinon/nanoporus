

def is_in_circle(radius_squared, center, x, y):
    return (x - center[0])**2 + (y - center[1])**2 <= radius_squared
def create_slice(radius, center, data_shape):
    MIN_Y = max(0, center[1] - radius)
    MAX_Y = min(data_shape[1], center[1] + radius)
    RADIUS_SQUARED = radius ** 2
    points_in_circle = []
    for x in range(max(0, center[0] - radius), min(data_shape[0], center[0] + radius)):
        for y in range(MIN_Y, MAX_Y):
            if is_in_circle(RADIUS_SQUARED, center, x, y):
                points_in_circle.append((x,y))
    return points_in_circle


def get_left_neighbour():
    pass
def get_up_neighbour():
    pass
def get_next_z_neighbour()

def create_lattice_neighoubr_graph(point, data, height, radius):
    graph = nx.Graph()
    nx.add_vertex(SOURCE_NODE)
    START_Z = max(0, point[2] - height)
    STOP_Z = min(data.shape[2], point[2] + height)
    # Add first layer of cylinder into the graph
    init_nodes = []
    # TODO:
    for z in range(START_Z, STOP_Z):
        for p in circle_slice:
            v = (p[0], p[1], z)
            graph.add_vertex(vertex)
            left_neighbour =  get_left_neighbour(v)
            if not left_neighbour == None
                graph.add_edge(v, left_neighbour, capcity = 1)
            up_neighbour =  get_up_neighbour(v)
            if not up_neighbour == None
                graph.add_edge(v, up_neighbour, capcity = 1)
            graph.add_edge(v, get_next_z_neighbour(v), capcity = 1)

    graph.add_vertex(SINK_NODE)
    return graph
