from bestResponse import bestResponse
import networkx as nx

if __name__ == '__main__':
    G = nx.read_gpickle("../test/graph3.pickle")
    n = G.number_of_nodes() - 1
    alpha = 3
    beta = 10
    print(bestResponse(G, n, alpha, beta))
