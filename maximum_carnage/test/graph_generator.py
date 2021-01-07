import networkx as nx
import os
from maximum_carnage.src.utils.graph_utils import drawNetwork


def forest_equilibrium():
    G = nx.DiGraph()
    G.add_edge(0, 1)
    G.add_edge(1, 2)
    G.add_edge(2, 3)

    G.add_edge(5, 4)
    G.add_edge(6, 4)
    G.add_edge(7, 4)

    G.add_edge(9, 8)
    G.add_edge(10, 8)
    G.add_edge(11, 8)

    G.add_edge(12, 13)
    G.add_edge(13, 14)
    G.add_edge(14, 15)

    for node in G:
        G.nodes[node]['immunization'] = False

    return G


def cycle_equilibrium():
    G = nx.DiGraph()
    n = 7
    for i in range(0, n):
        G.add_edge(i, i + 1)
    G.add_edge(n, 0)
    for node in G:
        G.nodes[node]['immunization'] = True if node % 2 == 0 else False

    return G


def flower_equilibrium():
    G = nx.DiGraph()
    G.add_edge(1, 0)
    G.add_edge(2, 0)
    G.add_edge(3, 0)
    G.add_edge(4, 0)
    G.add_edge(5, 0)
    G.add_edge(6, 0)
    G.add_edge(7, 0)
    G.add_edge(8, 0)

    G.add_edge(1, 9)
    G.add_edge(2, 9)
    G.add_edge(3, 10)
    G.add_edge(4, 10)
    G.add_edge(5, 11)
    G.add_edge(6, 11)
    G.add_edge(7, 12)
    G.add_edge(8, 12)
    for node in G:
        if node > 8 or node == 0:
            G.nodes[node]['immunization'] = True
        else:
            G.nodes[node]['immunization'] = False
    return G


def complete_bipartite_equilibrium():
    G = nx.DiGraph()
    G.add_edge(7, 0)
    G.add_edge(7, 1)
    G.add_edge(7, 2)
    G.add_edge(7, 3)
    G.add_edge(7, 4)
    G.add_edge(7, 5)
    G.add_edge(7, 6)

    G.add_edge(8, 0)
    G.add_edge(8, 1)
    G.add_edge(8, 2)
    G.add_edge(8, 3)
    G.add_edge(8, 4)
    G.add_edge(8, 5)
    G.add_edge(8, 6)

    for node in G:
        if node < 7:
            G.nodes[node]['immunization'] = True
        else:
            G.nodes[node]['immunization'] = False
    return G


if __name__ == '__main__':
    G = forest_equilibrium()
    H = cycle_equilibrium()
    Y = flower_equilibrium()
    K = complete_bipartite_equilibrium()

    nx.write_gpickle(G, os.path.dirname(os.path.abspath(__file__)) + './forest.pickle')
    nx.write_gpickle(H, os.path.dirname(os.path.abspath(__file__)) + './cycle.pickle')
    nx.write_gpickle(Y, os.path.dirname(os.path.abspath(__file__)) + './flower.pickle')
    nx.write_gpickle(K, os.path.dirname(os.path.abspath(__file__)) + './complete_bipartite.pickle')
