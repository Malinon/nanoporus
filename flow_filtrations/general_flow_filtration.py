import numpy as np
import networkx as nx
from .common_flow import SOURCE_NODE, SINK_NODE

def gen_flow_filtration(data, grapher):
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
                filtration[i,j,k], _ = nx.maximum_flow(grapher((i, j, k), data), SOURCE_NODE, SINK_NODE)
    return filtration

                
