#from PossibleStrategy.MetaTreeConstruct.MetaTreeConstruct import constructMetaTree
from PossibleStrategy.MetaTreeConstruct.MetaTreeConstruct2 import constructMetaTree
from PossibleStrategy.MetaTreeConstruct.ComponentsCollapse import collapse_graph
from utils.graph_utils import drawNetwork, renameGraph

import numpy as np
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt


if __name__=="__main__":
    G = nx.Graph()
    G.add_edge(1, 0)
    G.add_edge(1, 2)
    G.add_edge(1, 3)
    G.add_edge(3, 4)
    G.add_edge(4, 5)
    G.add_edge(5, 6)
    G.add_edge(5, 10)
    G.add_edge(6, 9)
    G.add_edge(6, 8)
    G.add_edge(6, 7)
    G.add_edge(10, 11)
    G.add_edge(10, 12)
    G.add_edge(11, 13)
    G.add_edge(13, 14)
    G.add_edge(15, 16)
    G.add_edge(14, 15)
    G.add_edge(15, 12)
    G.add_edge(16, 17)
    G.add_edge(16, 20)
    G.add_edge(17, 18)
    G.add_edge(17, 19)
    G.add_edge(19, 21)
    G.add_edge(20, 22)
    G.add_edge(21, 22)
    G.add_edge(22, 23)
    G.add_edge(12, 24)
    G.add_edge(24, 25)
    G.add_edge(26, 25)
    G.add_edge(27, 25)
    G.add_edge(28, 25)
    
    n = G.number_of_nodes()

    for i in range(n):
        G.nodes[i]['immunization'] = False

    G.nodes[3]['immunization'] = True
    G.nodes[5]['immunization'] = True
    G.nodes[7]['immunization'] = True
    G.nodes[11]['immunization'] = True
    G.nodes[15]['immunization'] = True
    G.nodes[16]['immunization'] = True
    G.nodes[21]['immunization'] = True
    G.nodes[25]['immunization'] = True

    [G, C_D, I] = collapse_graph(G, 3)

    #G = constructMetaTree(G, I)
    
    [G, D] = renameGraph(G)

    drawNetwork(G)

    #Immunized = [k for (k, v) in nx.get_node_attributes(G, 'immunization').items() if v is True]
    
    constructMetaTree(G)
    
