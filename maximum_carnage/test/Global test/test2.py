from maximum_carnage.src.bestResponse import bestResponse
from maximum_carnage.src.utils.graph_utils import paintTarget, utility_s
from maximum_carnage.test.utils.utils import drawNetwork
import networkx as nx
import itertools


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
    G = nx.read_gpickle("complete_bipartite.pickle")
    dict_size = {n: 1 for n in G.nodes()}
    nx.set_node_attributes(G, dict_size, 'size')
    alpha = G.nodes[0]['alpha']
    beta = G.nodes[0]['beta']

    G2 = G.to_undirected()
    G3 = G2.copy()
    tempt = []

    for i in range(0, G.number_of_nodes() + 1):
        aux = list(range(0, G.number_of_nodes() + 1))
        aux.remove(i)
        for L in range(0, G.number_of_nodes() + 1):
            for subset in itertools.combinations(aux, L):
                tempt.append(list(subset))

    print(tempt)
