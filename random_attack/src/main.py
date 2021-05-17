from bestResponse import bestResponse
import networkx as nx
from random_attack.src.utils.graph_utils import drawNetwork


if __name__ == '__main__':
    G = nx.read_gpickle("../test/Global test/cycle.pickle")
    drawNetwork(G)
    n = G.number_of_nodes() - 1
    alpha = 1/2
    beta = 1/2
    print(bestResponse(G, 0, alpha, beta))
