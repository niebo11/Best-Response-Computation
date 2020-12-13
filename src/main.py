from main2 import bestResponse
import networkx as nx

if __name__ == '__main__':
    G = nx.read_gpickle("../test/graph1.pickle")
    alpha = 5/2
    bestResponse(G, 75, alpha, 0)
