import networkx as nx
from .common_flow import SOURCE_NODE, SINK_NODE, create_slice, is_in_circle

def get_left_neighbour(vertex, center, radius_squared, shape):
    if is_in_circle(radius_squared, center, vertex[0] + 1, vertex[1]) and shape[0] >  vertex[0] + 1:
        return (vertex[0] + 1, vertex[1], vertex[2])

def get_up_neighbour(vertex, center, radius_squared, shape):
    if is_in_circle(radius_squared, center, vertex[0] , vertex[1] + 1) and shape[1] >  vertex[1] + 1:
        return (vertex[0], vertex[1] + 1, vertex[2])

def get_next_z_neighbour(vertex):
    """ get lattice neighbour of given vertex in z direction"""
    return (vertex[0], vertex[1], vertex[2] + 1)

def update_graph_by_slice(graph, radius_squared, circle_slice, z, stop_z, center, data):
    """
    Update the graph by adding nodes and edges for a given slice.
    """
    sh = data.shape
    for p in circle_slice:
        if data[p[0], p[1], z]:
            v = (p[0], p[1], z)
            graph.add_node(v)
            left_neighbour =  get_left_neighbour(v, center, radius_squared, sh)
            if not left_neighbour == None and data[left_neighbour[0], left_neighbour[1], left_neighbour[2]]:
                graph.add_edge(v, left_neighbour, capacity = 1)
            up_neighbour =  get_up_neighbour(v, center, radius_squared, sh)
            if not up_neighbour == None and data[up_neighbour[0], up_neighbour[1], up_neighbour[2]]:
                graph.add_edge(v, up_neighbour, capacity = 1)
            if z < stop_z:
                z_neighbour = get_next_z_neighbour(v)
                if data[z_neighbour[0], z_neighbour[1], z_neighbour[2]]:
                    graph.add_edge(v, z_neighbour, capacity = 1) 

def create_lattice_neighoubr_graph(point, data, height, radius):
    """
    Create a graph inside cylinder centered at given point.
    Main axis of cylinder is z axis. (Direction of stress)
    ----------
    point: tuple
        The point around which the cylinder is centered
    data: numpy array
        The data describing material
    height: int
        The height of the cylinder
    radius: int
        The radius of the cylinder
    """
    graph = nx.Graph()
    graph.add_node(SOURCE_NODE)
    START_Z = max(0, point[2] - height)
    STOP_Z = min(data.shape[2] - 1, point[2] + height)
    CENTER = (point[0], point[1])
    RADIUS_SQUARED = radius ** 2
    circle_slice = create_slice(radius, CENTER, data.shape)
    for z in range(START_Z, STOP_Z + 1):
        update_graph_by_slice(graph, RADIUS_SQUARED, circle_slice, z, STOP_Z, CENTER, data)
    # Add connection of first slice with source (infinit capacity)
    for p in circle_slice:
        if data[p[0], p[1], START_Z]:
            graph.add_edge((p[0], p[1], START_Z), SOURCE_NODE, capacity=2)
    # Add last slice with sink
    graph.add_node(SINK_NODE)
    for p in circle_slice:
        if data[p[0], p[1], STOP_Z]:
            graph.add_edge((p[0], p[1], STOP_Z), SINK_NODE, capacity=2)
    return graph
