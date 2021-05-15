from maximum_carnage.src.bestResponse import bestResponse
from maximum_carnage.src.utils.graph_utils import paintTarget, utility_s
from maximum_carnage.test.utils.utils import drawNetwork
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
    G = nx.read_gpickle("flower.pickle")
    dict_size = {n: 1 for n in G.nodes()}
    nx.set_node_attributes(G, dict_size, 'size')
    alpha = G.nodes[0]['alpha']
    beta = G.nodes[0]['beta']

    G2 = G.to_undirected()
    G3 = G2.copy()

    for i in range(0, G.number_of_nodes()):
        print("--------------------------------------")
        ini_u = initial_utility(G, i, alpha, beta)
        G.nodes[i]['profit'] = ini_u
        BR = bestResponse(G.copy(), i, alpha, beta)
        G3.nodes[i]['profit'] = BR[1]
        print("node :", i)
        print("initial strategy utility: ", ini_u, "calculated BR utility :", BR[1])
        if BR[1] > ini_u:
            print(BR[0])
        print(BR[0])
        G4 = G.copy()
        G4.remove_edges_from([(i, neighbor) for neighbor in G4.adj[i]])
        nx.set_node_attributes(G4, {i: BR[0][1]}, 'immunization')
        for item in BR[0][0]:
            G4.add_edge(i, item)
        for j in range(0, G.number_of_nodes()):
            G4.nodes[j]['profit'] = initial_utility(G4, j, alpha, beta)

    drawNetwork(G, [], 'flower.png', profit=True)
