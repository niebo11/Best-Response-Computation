from utils.graph_utils import drawNetwork, renameGraph
from PossibleStrategy.PossibleStrategy import Utility

import time
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
    
    '''
    G.add_edge(0, 1)
    G.add_edge(1, 2)
    G.add_edge(1, 3)
    G.add_edge(2, 4)
    G.add_edge(3, 4)
    G.add_edge(4, 5)
    '''
    
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
    
    '''
    G.nodes[0]['immunization'] = True
    G.nodes[2]['immunization'] = True
    G.nodes[3]['immunization'] = True
    G.nodes[5]['immunization'] = True
    '''

    [G, C_D, I] = collapse_graph(G, 3)
    
    time1 = time.perf_counter()
    G1 = constructMetaTree(G, I)
    time2 = time.perf_counter()
    
    [G1, mapping] = renameGraph(G1)
    
    #print('constructMetaTree used: ' + str(time2-time1) + 'seconds')
    
    #drawNetwork(G1)
    
    #for g in G1:
        #res = "node " +  str(g) + "   size:" + str(G1.nodes[g]['size']) + "\n"
        #print(res)

    M = nx.Graph()

    M.add_edge(3, 1)
    M.add_edge(1, 0)
    M.add_edge(0, 2)
    M.add_edge(2, 4)
    M.add_edge(2, 5)
    M.add_edge(5, 6)
    M.add_edge(6, 7)
    M.add_edge(6, 8)

    M.nodes[0]['size'] = 6
    M.nodes[1]['size'] = 3
    M.nodes[2]['size'] = 3
    M.nodes[3]['size'] = 1
    M.nodes[4]['size'] = 12
    M.nodes[5]['size'] = 4
    M.nodes[6]['size'] = 3
    M.nodes[7]['size'] = 6
    M.nodes[8]['size'] = 5

    for i in range(0, 8):
        M.nodes[i]['immunization'] = False

    M.nodes[0]['immunization'] = True
    M.nodes[3]['immunization'] = True
    M.nodes[4]['immunization'] = True
    M.nodes[5]['immunization'] = True
    M.nodes[7]['immunization'] = True
    M.nodes[8]['immunization'] = True

    MetaTreeSelect(M, 6, 15)
