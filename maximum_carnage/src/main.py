from bestResponse import bestResponse
from utils.graph_utils import drawNetwork, paintTarget, utility_s
import networkx as nx


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
    G = nx.read_gpickle("../test/Global test/cycle.pickle")
    alpha = G.nodes[0]['alpha']
    beta = G.nodes[0]['beta']
    drawNetwork(G)

    for i in range(0, G.number_of_nodes()):
        print("--------------------------------------")
        ini_u = initial_utility(G, i, alpha, beta)
        BR = bestResponse(G.copy(), i, alpha, beta)
        print("node :", i)
        print("initial strategy utility: ", ini_u, "calculated BR utility :", BR[1])
        if BR[1] > ini_u:
            print(BR[0])
