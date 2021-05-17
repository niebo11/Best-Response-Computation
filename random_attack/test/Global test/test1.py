import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':
    G = nx.read_gpickle("graph1.pickle")
    print(G.edges())
    nx.draw_spring(G)
    plt.plot()
