import networkx as nx
from random_attack.src.UniformSubSetSelect.UniformSubSetSelect import uniformSubSetSelect
import unittest
from random_attack.test.utils.utils import constructCu, drawNetwork, graphFromList, collapse_graph, renameGraph, \
    translate


class testSubSetSelect(unittest.TestCase):

    @unittest.skip("reason for skipping")
    def test_emptyset(self):
        for i in range(2, 5):
            max_T = 1
            k = 5
            P = 1.0 - (max_T / i)
            Cu = [[x] for x in range(1, i + 1)]
            # Case where our elements are all targeted
            U = uniformSubSetSelect(len(Cu), i + 1, Cu, 0.1)
            U = uniformSubSetSelect(len(Cu), i, Cu, 0.1)

    def test_custom(self):
        max_T, Cu = constructCu()
        U = uniformSubSetSelect(len(Cu), max_T, Cu, 0.1)
        print(Cu)
        print(max_T)
        print(U)

        G = graphFromList(Cu).to_undirected()
        G2, I, C_D = collapse_graph(G)
        G2, R_D = renameGraph(G2)
        drawNetwork(G2, [], 'test1.1.png')
        #
        bought1 = translate(U, C_D, R_D)
        # bought2 = translate(Av, C_D, R_D)
        drawNetwork(G2, bought1, 'test1.2.png')
        # drawNetwork(G2, bought2, 'test1.3.png')


if __name__ == '__main__':
    unittest.main()
