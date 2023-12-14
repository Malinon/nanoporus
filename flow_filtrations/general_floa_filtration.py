

SOURCE_NODE = 0
SINK_NODE = 1

class GraphOrFlow:
    def __init__(is_flow, data):
        self.data = data



def gen_flow_filtration(data, grapher):
    filtration = np.array(shape=data.shape, dtype=float)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            for k in range(data.shape[2]):
                graph_or_flow = grapher((i, j, k), data)
                if graph_or_flow.is_flow:
                    filtration[i,j,k] = graph_or_flow
                else:
                    filtration[i,j,k] = nx.max_flow(graph_or_flow, SOURCE_NODE, SINK_NODE)
    return filtration

                