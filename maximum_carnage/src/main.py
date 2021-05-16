from bestResponse import bestResponse
from utils.graph_utils import initial_utility
import networkx as nx


if __name__ == '__main__':
    # read a Game State G(S, I) from a pickle
    G = nx.read_gpickle("../test/Global test/Nash Equilibrium networks/cycle.pickle")

    # Set up the parameters alpha and beta
    alpha = G.nodes[0]['alpha']
    beta = G.nodes[0]['beta']

    # For each player computes the initial utility and the Best Response, compare their result, if it is different
    # print the difference.
    for i in range(0, G.number_of_nodes()):
        print("--------------------------------------")
        ini_u = initial_utility(G, i, alpha, beta)
        BR = bestResponse(G.copy(), i, alpha, beta)
        print("node :", i)
        print("initial strategy utility: ", ini_u, "calculated BR utility :", BR[1])
        if BR[1] > ini_u:
            print(BR[0])
