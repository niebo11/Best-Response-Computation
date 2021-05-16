from maximum_carnage.src.bestResponse import bestResponse
from maximum_carnage.src.utils.graph_utils import initial_utility
from maximum_carnage.test.utils.utils import drawNetwork, randomGraph3
import networkx as nx
import itertools
import os


if __name__ == '__main__':
    test = True
    iteration = 0
    while test:
        print('##########iteration ' + str(iteration) + '############')
        iteration += 1
        n = 20
        G = randomGraph3(n, 1/n)
        drawNetwork(G, [], 'graphs/images/graph_' + str(n) + '_' + str(iteration) + '.png')
        #
        nx.write_gpickle(G, os.path.dirname(os.path.abspath(__file__)) + './graphs/pickle/graph_' + str(n) + '_' +
                         str(iteration) + '.pickle')
        alpha = 0.5
        beta = 3

        for i in range(0, G.number_of_nodes()):
            G2 = G.copy()
            print('------------ node' + str(i) + ' -------------')
            strategies = []
            utilities = []
            utilities2 = []
            aux = list(range(0, G.number_of_nodes()))
            aux.remove(i)
            for L in range(0, G.number_of_nodes()):
                for subset in itertools.combinations(aux, L):
                    strategies.append(list(subset))
            current_strategy = [(i, k) for k in G.adj[i]]
            G2.remove_edges_from(current_strategy)
            for item in strategies:
                G3 = G2.copy()
                new_strategy = [(i, k) for k in item]
                G3.add_edges_from(new_strategy)
                utilities.append(initial_utility(G3, i, alpha, beta))
            for item in strategies:
                G3 = G2.copy()
                G3.nodes[i]['immunization'] = not G3.nodes[i]['immunization']
                new_strategy = [(i, k) for k in item]
                G3.add_edges_from(new_strategy)
                utilities2.append(initial_utility(G3, i, alpha, beta))
            BR = bestResponse(G.copy(), i, alpha, beta)
            G3 = G2.copy()
            new_strategy = ((i, k) for k in BR[0][0])
            G3.nodes[i]['immunization'] = BR[0][1]
            G3.add_edges_from(new_strategy)
            BR_utility = initial_utility(G3, i, alpha, beta)
            max_utility = max(utilities)
            max_utility2 = max(utilities2)
            print(BR)
            if max_utility > max_utility2:
                print(strategies[utilities.index(max_utility)], max_utility, G.nodes[i]['immunization'])
            else:
                print(strategies[utilities2.index(max_utility2)], max_utility2, not G.nodes[i]['immunization'])
            if BR_utility != max(max_utility, max_utility2):
                test = False
            if iteration == 10:
                test = False
