import networkx as nx
from maximum_carnage.src.SubSetSelect.SubSetSelect import subSetSelect
import unittest
from maximum_carnage.test.utils.utils import constructCu, drawNetwork, graphFromList, collapse_graph, renameGraph, \
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
            At, Av = subSetSelect(len(Cu), i + 1, Cu, 0.1)
            self.assertEqual(At, Cu, 'At')
            self.assertEqual(Av, Cu, 'Av')
            At, Av = subSetSelect(len(Cu), i, Cu, 0.1)
            self.assertEqual(At, Cu, 'At2')
            self.assertEqual(Av, Cu[:-1], 'Av2')

    def test_custom(self):
        max_T, T_size, Cu = constructCu()
        At, Av = subSetSelect(len(Cu), T_size - 1, Cu, 5)

        print('T_size', T_size)
        print('Av total size: ', 1 + sum(list(map(lambda x: len(x), Av))))
        print('At total size: ', 1 + sum(list(map(lambda x: len(x), At))))

        G = graphFromList(Cu).to_undirected()
        G2, I, C_D = collapse_graph(G)
        G2, R_D = renameGraph(G2)
        drawNetwork(G2, [], 'test1.1.png')

        bought1 = translate(At, C_D, R_D)
        bought2 = translate(Av, C_D, R_D)
        drawNetwork(G2, bought1, 'test1.2.png')
        drawNetwork(G2, bought2, 'test1.3.png')


if __name__ == '__main__':
    unittest.main()
