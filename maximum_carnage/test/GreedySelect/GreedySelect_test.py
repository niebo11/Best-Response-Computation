import json
import random as rd
import time
import unittest

import matplotlib.pyplot as plt
import numpy as np

from maximum_carnage.src.GreedySelect.GreedySelect import greedySelect, greedySelect2
from maximum_carnage.test.utils.utils import graphFromList, collapse_graph, drawNetwork, renameGraph, translate, \
    constructCu


# def test_empty(Cu, n, T_size, max_T, alpha):
#     # if os.path.exists(os.path.dirname(os.path.abspath(__file__)) + './graphs/empty_graph_' + str(n) +
#     #                   '.pickle'):
#     #     G = nx.read_gpickle(os.path.dirname(os.path.abspath(__file__)) + './graphs/empty_graph_' +
#     #                         str(n) + '.pickle')
#     # else:
#     #     G = emptyGraph(n)
#     # pos = nx.nx_pydot.graphviz_layout(G)
#
#     response = greedySelect(Cu, max_T, T_size, alpha)
#     return response
#
#     # nx.draw_networkx(G, pos)
#     # plt.show()
#     # plt.savefig('networkx_graph.png')

class testGreedySelect(unittest.TestCase):
    @unittest.skip("reason for skipping")
    def test_emptyset(self):
        x_line = []
        y_new = []
        y_old = []
        for i in range(2, 300000, 500):
            x_line.append(i)
            max_T = 1
            k = 5
            P = 1.0 - (max_T / i)
            print(P, i)
            Cu = [[x] for x in range(1, i + 1)]
            start = time.time()
            # Case where our elements are all targeted
            self.assertEqual(greedySelect(Cu, max_T, i, P + 1), [], 'When alpha is greater test failed!')
            self.assertEqual(greedySelect(Cu, max_T, i, P / 2), Cu, 'When alpha is smaller test failed!')
            # TODO add documentation special case
            # self.assertEqual(greedySelect(Cu, max_T, i, P), [], 'When alpha is equal test failed!')

            # Case where our elements are never targeted
            self.assertEqual(greedySelect(Cu, k, i + k, rd.uniform(2, 100)), [], 'N')
            self.assertEqual(greedySelect(Cu, k, i + k, rd.uniform(0, 0.99)), Cu, 'IDK2')
            end = time.time()

            y_new.append(end - start)

            start = time.time()
            # Case where our elements are all targeted
            self.assertEqual(greedySelect2(Cu, max_T, i, P + 1), [], 'When alpha is greater test failed!')
            self.assertEqual(greedySelect2(Cu, max_T, i, P / 2), Cu, 'When alpha is smaller test failed!')
            # TODO add documentation special case
            # self.assertEqual(greedySelect2(Cu, max_T, i, P), [], 'When alpha is equal test failed!')

            # Case where our elements are never targeted
            self.assertEqual(greedySelect2(Cu, k, i + k, rd.uniform(2, 100)), [], 'N')
            self.assertEqual(greedySelect2(Cu, k, i + k, rd.uniform(0, 0.99)), Cu, 'IDK2')
            end = time.time()
            y_old.append(end - start)

        m, b = np.polyfit(x_line, y_new, 1)
        plt.plot(x_line, m * np.asarray(x_line) + b, 'r', label='GreedySelect modified')
        m2, b2 = np.polyfit(x_line, y_old, 1)
        plt.plot(x_line, m2 * np.asarray(x_line) + b2, 'b', label='GreedySelect original')
        plt.legend(loc='best')
        plt.xlabel('Number of nodes')
        plt.ylabel('Time of milliseconds')

        plt.show()
        with open('test_result.txt', 'w') as outfile:
            json.dump({
                'time': x_line,
                'new_greedy': y_new,
                'old_greedy': y_old
            }, outfile)

    def test_nonEmptySet(self):
        Cu_mock = [[13], [14], [15],
                   [16, 17], [18, 19],
                   [20, 21, 22], [23, 24, 25],
                   [1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12],
                   [26, 27, 28, 29, 30]]

        G = graphFromList(Cu_mock).to_undirected()
        G2, I, C_D = collapse_graph(G)
        G2, R_D = renameGraph(G2)
        drawNetwork(G2, [], 'test images/abcd.png')

        max_T = 5

        T_size = 5
        # greedyselect 1
        response1 = greedySelect(Cu_mock, max_T, T_size, rd.uniform(0, 0.99))
        bought = translate(response1, C_D, R_D)
        drawNetwork(G2, bought, 'test images/abcd2.png')

        Cu_mock += [[31, 32, 33, 34, 35], [36, 37, 38, 39, 40]]

        T_size = 15

        G = graphFromList(Cu_mock).to_undirected()
        G2, I, C_D = collapse_graph(G)
        G2, R_D = renameGraph(G2)
        drawNetwork(G2, [], 'test images/test2.png')

        # greedyselect 2
        response2 = greedySelect(Cu_mock, max_T, T_size, 1)
        bought2 = translate(response2, C_D, R_D)
        drawNetwork(G2, bought2, 'test images/test2.1.png')

    def test_custom(self):
        max_T, T_size, Cu = constructCu()

        G = graphFromList(Cu).to_undirected()
        G2, I, C_D = collapse_graph(G)
        G2, R_D = renameGraph(G2)
        drawNetwork(G2, [], 'test images/test1.0.png')

        print(max_T)

        Loop = True
        index = 1

        while Loop:
            alpha = float(input('Introduce an alpha to test: '))
            response1 = greedySelect(Cu, max_T, T_size, alpha)
            bought = translate(response1, C_D, R_D)
            drawNetwork(G2, bought, 'test images/test1.' + str(index) + '.png')
            index += 1
            Loop = int(input('Introduce 1 if you want to try again, otherwise introduce 0: '))


if __name__ == '__main__':
    unittest.main()
