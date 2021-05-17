import networkx as nx
import os


def emptyGraph(n):
    G = nx.DiGraph()
    for node in range(n):
        G.add_node(node)
        G.nodes[node]['immunization'] = False

    unique = 1

    # while os.path.exists(os.path.dirname(os.path.abspath(__file__)) + './graphs/empty_graph_' + str(n) +
    #                      '_' + str(unique) + '.pickle'):
    #     unique += 1
    #
    #nx.write_gpickle(G, os.path.dirname(os.path.abspath(__file__)) + './graphs/empty_graph_' + str(n) +
    #                 '.pickle')
    return G
