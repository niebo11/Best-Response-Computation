import networkx as nx
import matplotlib.pyplot as plt
from maximum_carnage.src.PossibleStrategy.MetaTreeSelect.MetaTreeSelect import subTreeSize, root_tree
import unittest
import jgraph as ig


class testSubTreeSize(unittest.TestCase):

    Graph_Simple = nx.Graph()
    Graph_Simple.add_edge(0, 1)
    Graph_Simple.add_edge(1, 2)
    Graph_Simple.add_edge(1, 3)

    Graph_Simple.nodes[0]['size'] = 1
    Graph_Simple.nodes[1]['size'] = 1
    Graph_Simple.nodes[2]['size'] = 1
    Graph_Simple.nodes[3]['size'] = 1

    def test_level_function(self):
        visited = [False] * self.Graph_Simple.number_of_nodes()
        level_dict = root_tree(self.Graph_Simple, 0, visited, {}, 0)
        self.assertEqual(level_dict, {0: 0, 1: 1, 2: 2, 3: 2}, 'level dictionary')

    def test_single_node(self):
        g = ig.Graph.from_networkx(self.Graph_Simple)
        layout = g.layout()
        ig.plot(g, layout=layout)
        # pos = nx.nx_pydot.graphviz_layout(self.Graph_Simple, root=0)
        # nx.draw_networkx(self.Graph_Simple, pos)
        plt.show()

        visited = [False] * self.Graph_Simple.number_of_nodes()
        leaf = [x for x in self.Graph_Simple.nodes if self.Graph_Simple.degree[x] == 1]
        sub_tree_sizes = [{} for _ in self.Graph_Simple.nodes]
        level_dict = root_tree(self.Graph_Simple, 0, visited, {}, 0)

        subTreeSize(self.Graph_Simple, sub_tree_sizes, leaf, level_dict)
        self.assertEqual(sub_tree_sizes[0], {1: 1}, 'node 0')
        self.assertEqual(sub_tree_sizes[1], {0: 3, 2: 3, 3: 3}, 'node 1')
        self.assertEqual(sub_tree_sizes[2], {1: 1}, 'node 2')
        self.assertEqual(sub_tree_sizes[3], {1: 1}, 'node 3')


if __name__ == '__main__':
    unittest.main()
