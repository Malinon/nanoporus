import numpy as np
import networkx as nx
from .common_flow import SOURCE_NODE, SINK_NODE

def gen_flow_filtration(data, grapher, flow_func=nx.maximum_flow_value):
    """
    Generate a flow filtration for a given data and graph generating function
    
    Parameters
    ----------
    data: numpy array
        The data describing material
    grapher: function
        A function that generates a graph given a point and data
    """
    filtration = np.empty(shape=data.shape, dtype=float)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            for k in range(data.shape[2]):
                filtration[i,j,k] = flow_func(grapher((i, j, k), data), SOURCE_NODE, SINK_NODE)
    return filtration

def gen_avg_direction_flow_filtration(graph, source_node, sink_node, graph_shape):
    filtration_value, edge_flow = nx.maximum_flow(graph, source_node, sink_node)
    starting_nodes = set(node for node in graph.neighbors(source_node))
    end_nodes = set(node for node in graph.neighbors(sink_node))
    input_weighed_avg = [0, 0, 0]
    output_weighed_avg = [0, 0, 0]
    for node in starting_nodes:
            for i in range(3):
                input_weighed_avg[i] += edge_flow[source_node][node] * (node[i])
    for node in end_nodes:
        for i in range(3):
            output_weighed_avg[i] += edge_flow[node][sink_node] * (node[i])
    return tuple((output_weighed_avg[i] - input_weighed_avg[i]) for i in range(3))
                
