from maximum_carnage.src.bestResponse import bestResponse
from maximum_carnage.src.utils.graph_utils import paintTarget, utility_s
from maximum_carnage.test.utils.utils import drawNetwork, randomGraph3
import networkx as nx
import itertools
import os
import random as rd


def initial_utility(G, v, alpha, beta):
    G_ini = G.to_undirected()
    G_ini.remove_nodes_from([node for node in G.nodes if G_ini.nodes[node]['immunization']])
    length_of_vulnerable_region = list(map(len, list(nx.connected_components(G_ini))))
    if len(length_of_vulnerable_region) > 0:
        size_T = max(length_of_vulnerable_region)
    else:
        size_T = 0
    G_ini = G.to_undirected()
    G_ini, max_T, R_t = paintTarget(G_ini, size_T)
    return utility_s(G_ini, v, R_t, max_T) - len(list(G.out_edges(v))) * alpha - G.nodes[v]['immunization'] * beta


if __name__ == '__main__':
    #
    # G = nx.read_gpickle("flower.pickle")
    # dict_size = {n: 1 for n in G.nodes()}
    # nx.set_node_attributes(G, dict_size, 'size')
    # alpha = G.nodes[0]['alpha']
    # beta = G.nodes[0]['beta']
    test = True
    iter = 0
    while test:
        print('##########iteration ' + str(iter) + '#############')
        iter += 1
        n = 100
        G = randomGraph3(n, 1/n)
        drawNetwork(G, [], 'graphs/images/graph_' + str(n) + '_' + str(iter) + '.png')
        nx.write_gpickle(G, os.path.dirname(os.path.abspath(__file__)) + './graphs/pickle/graph_' + str(n) + '_' +
                         str(iter) + '.pickle')
        alpha = 30
        beta = 7
        print('alpha: ', alpha, '/ beta: ', beta)

        for i in range(0, G.number_of_nodes()):
            G2 = G.copy()
            print('------------ node' + str(i) + ' -------------')
            strategies = []
            utilities = []
            utilities2 = []
            aux = list(range(0, G.number_of_nodes()))
            aux.remove(i)
            for L in range(0, int(G.number_of_nodes()/alpha)):
                for subset in itertools.combinations(aux, L):
                    strategies.append(list(subset))
            print(len(strategies))
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
                print(strategies[utilities2.index(max_utility2)],  not G.nodes[i]['immunization'], max_utility2)
            if BR_utility != max(max_utility, max_utility2):
                print('here')
                test = False
            if iter == 50:
                test = False