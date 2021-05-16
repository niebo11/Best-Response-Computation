from maximum_carnage.src.bestResponse import bestResponse
from maximum_carnage.src.utils.graph_utils import paintTarget, initial_utility
from maximum_carnage.test.utils.utils import drawNetwork
import networkx as nx

# test used to check NE
if __name__ == '__main__':
    G = nx.read_gpickle("Nash Equilibrium networks/cycle.pickle")

    # Set up some parameters
    dict_size = {n: 1 for n in G.nodes()}
    nx.set_node_attributes(G, dict_size, 'size')
    alpha = G.nodes[0]['alpha']
    beta = G.nodes[0]['beta']

    G2 = G.to_undirected().copy()

    for i in range(0, G.number_of_nodes()):
        print("--------------------------------------")
        ini_u = initial_utility(G, i, alpha, beta)
        G.nodes[i]['profit'] = ini_u
        BR = bestResponse(G.copy(), i, alpha, beta)
        G2.nodes[i]['profit'] = BR[1]
        print("node :", i)
        print("initial strategy utility: ", ini_u, "calculated BR utility :", BR[1])
        if ini_u > BR[1]:
            print(BR[0])

    # ~drawNetwork(G, [], 'flower.png', profit=True)
