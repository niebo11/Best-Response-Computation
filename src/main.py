from src.main2 import bestResponse
from utils.graph_utils import drawNetwork
import networkx as nx

if __name__ == '__main__':
    G = nx.read_gpickle("../test/graph1.pickle")
    alpha = 3
    bestResponse(G, 30, alpha)
