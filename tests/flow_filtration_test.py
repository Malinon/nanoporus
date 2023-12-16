import unittest
import sys
sys.path.append('../')

import numpy as np
import networkx as nx
from flow_filtrations import create_lattice_neighoubr_graph, SOURCE_NODE, SINK_NODE

class TestNeighbourLatticeFlow(unittest.TestCase):
    def test_empty_cylinder_flow(self):
        input_grid = np.full((50, 50, 50), False)
        graph = create_lattice_neighoubr_graph((25,25, 25), input_grid, 4, 2)
        self.assertEqual(nx.number_of_nodes(graph), 2)
        self.assertEqual(nx.number_of_edges(graph), 0)
        flow_value, _ = nx.maximum_flow(graph, SOURCE_NODE, SINK_NODE)
        self.assertEqual(flow_value, 0)

    def test_full_cylinder_flow(self):
        input_grid = np.full((50, 50, 50), True)
        graph = create_lattice_neighoubr_graph((25, 25, 25), input_grid, 4, 2)
        self.assertEqual(nx.number_of_nodes(graph), 13 * 9 + 2)
        self.assertEqual(nx.number_of_edges(graph), 16 * 9 + 10 * 13)
        flow_value, a = nx.maximum_flow(graph, SOURCE_NODE, SINK_NODE)
        self.assertEqual(flow_value, 13)

    def test_empty_slice_flow(self):
        input_grid = np.full((50, 50, 50), True)
        for x in range(50):
            for y in range(50):
                input_grid[x, y, 25] = False
        graph = create_lattice_neighoubr_graph((25,25, 25), input_grid, 4, 2)
        self.assertEqual(nx.number_of_nodes(graph), 13 * 8 + 2)
        self.assertEqual(nx.number_of_edges(graph), 16 * 8 + 8 * 13)
        flow_value, _ = nx.maximum_flow(graph, SOURCE_NODE, SINK_NODE)
        self.assertEqual(flow_value, 0)

    def test_on_edge_flow(self):
        input_grid = np.full((50, 50, 50), True)
        graph = create_lattice_neighoubr_graph((0, 0, 1), input_grid, 4, 2)
        self.assertEqual(nx.number_of_nodes(graph), 2 +  6 * 6)
        self.assertEqual(nx.number_of_edges(graph), 7 * 6 + 6 * 6)
        flow_value, _ = nx.maximum_flow(graph, SOURCE_NODE, SINK_NODE)
        self.assertEqual(flow_value, 6)

    def test_cylinder_with_missing_center_flow(self):
        input_grid = np.full((50, 50, 50), True)
        input_grid[25, 25, 25] = False
        graph = create_lattice_neighoubr_graph((25,25, 25), input_grid, 4, 2)
        self.assertEqual(nx.number_of_nodes(graph), 13 * 9 + 2 -1)
        self.assertEqual(nx.number_of_edges(graph), 16 * 9 + 10 * 13 - 4 - 2)
        flow_value, _ = nx.maximum_flow(graph, SOURCE_NODE, SINK_NODE)
        self.assertEqual(flow_value, 12)

    def test_zig_zag_flow(self):
        input_grid = np.full((50, 50, 50), False)
        # Make Zig zag path
        input_grid[25, 24, 23] = True
        input_grid[25, 24, 24] = True
        input_grid[25, 25, 24] = True
        input_grid[25, 25, 25] = True
        input_grid[26, 25, 25] = True
        input_grid[26, 26, 25] = True
        input_grid[26, 26, 26] = True
        input_grid[25, 26, 26] = True
        input_grid[25, 26, 27] = True
        graph = create_lattice_neighoubr_graph((25,25, 25), input_grid, 2, 2)
        self.assertEqual(nx.number_of_nodes(graph), 11)
        self.assertEqual(nx.number_of_edges(graph), 10)
        flow_value, _ = nx.maximum_flow(graph, SOURCE_NODE, SINK_NODE)
        self.assertEqual(flow_value, 1)

if __name__ == '__main__':
    unittest.main()