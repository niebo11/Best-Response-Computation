import networkx as nx
from maximum_carnage.test.utils.utils import drawNetwork2
from maximum_carnage.src.PossibleStrategy.MetaTreeConstruct.MetaTreeConstruct import constructMetaTree

G = nx.Graph()

G.add_node(0)
G.nodes[0]['immunization'] = False
G.nodes[0]['target'] = True

G.add_edge(0, 1)
G.nodes[1]['immunization'] = True
G.nodes[1]['target'] = False

G.add_edge(1, 2)
G.add_edge(1, 3)

G.nodes[2]['immunization'] = False
G.nodes[2]['target'] = False

G.nodes[3]['immunization'] = False
G.nodes[3]['target'] = False

G.add_edge(2, 4)
G.add_edge(3, 4)

G.nodes[4]['immunization'] = True
G.nodes[4]['target'] = False

G.add_edge(4, 5)
G.add_edge(5, 6)

G.nodes[5]['immunization'] = False
G.nodes[5]['target'] = False

G.nodes[6]['immunization'] = True
G.nodes[6]['target'] = False

G.add_edge(6, 7)
G.add_edge(6, 8)

G.nodes[7]['immunization'] = False
G.nodes[7]['target'] = True

G.nodes[8]['immunization'] = False
G.nodes[8]['target'] = True

G.add_edge(7, 9)
G.add_edge(8, 9)

G.nodes[9]['immunization'] = True
G.nodes[9]['target'] = False

G.add_edge(9, 10)
G.add_edge(10, 11)

G.nodes[10]['immunization'] = False
G.nodes[10]['target'] = False

G.nodes[11]['immunization'] = True
G.nodes[11]['target'] = False

G.add_edge(11, 12)
G.add_edge(11, 13)
G.add_edge(14, 12)
G.add_edge(14, 13)

G.nodes[12]['immunization'] = False
G.nodes[12]['target'] = True

G.nodes[13]['immunization'] = False
G.nodes[13]['target'] = True

G.nodes[14]['immunization'] = True
G.nodes[14]['target'] = False

# G.add_edge(14, 15)
G.add_edge(15, 48)

G.nodes[15]['immunization'] = False
G.nodes[15]['target'] = True

G.add_edge(15, 16)
G.add_edge(16, 17)
G.add_edge(17, 18)

G.nodes[16]['immunization'] = True
G.nodes[16]['target'] = False

G.nodes[17]['immunization'] = False
G.nodes[17]['target'] = False

G.nodes[18]['immunization'] = True
G.nodes[18]['target'] = False

G.add_edge(18, 19)
G.add_edge(18, 20)

G.nodes[19]['immunization'] = False
G.nodes[19]['target'] = True

G.nodes[20]['immunization'] = False
G.nodes[20]['target'] = True

# G.add_edge(19, 21)
G.add_node(21)

G.nodes[21]['immunization'] = True
G.nodes[21]['target'] = False

G.add_edge(21, 22)
G.add_edge(21, 23)
G.add_edge(21, 24)
G.add_edge(22, 25)
G.add_edge(23, 25)
G.add_edge(24, 25)

G.nodes[22]['immunization'] = False
G.nodes[22]['target'] = True
G.nodes[23]['immunization'] = False
G.nodes[23]['target'] = True
G.nodes[24]['immunization'] = False
G.nodes[24]['target'] = True

G.nodes[25]['immunization'] = True
G.nodes[25]['target'] = False

G.add_edge(25, 26)
G.add_edge(25, 27)
G.add_edge(25, 28)

G.nodes[26]['immunization'] = False
G.nodes[26]['target'] = True

G.nodes[27]['immunization'] = False
G.nodes[27]['target'] = False

G.nodes[28]['immunization'] = False
G.nodes[28]['target'] = False

G.add_edge(28, 29)

G.nodes[29]['immunization'] = True
G.nodes[29]['target'] = False

G.add_edge(29, 30)

G.nodes[30]['immunization'] = False
G.nodes[30]['target'] = True

G.add_edge(30, 31)
G.add_edge(30, 32)
G.add_edge(30, 33)
G.add_edge(33, 19)

G.nodes[31]['immunization'] = True
G.nodes[31]['target'] = False
G.nodes[32]['immunization'] = True
G.nodes[32]['target'] = False
G.nodes[33]['immunization'] = True
G.nodes[33]['target'] = False

G.add_edge(32, 34)
G.add_edge(34, 35)
G.add_edge(35, 36)

G.nodes[34]['immunization'] = False
G.nodes[34]['target'] = False
G.nodes[35]['immunization'] = True
G.nodes[35]['target'] = False
G.nodes[36]['immunization'] = False
G.nodes[36]['target'] = False

G.add_edge(33, 37)
G.add_edge(33, 38)
G.add_edge(33, 39)
G.add_edge(33, 40)

G.nodes[37]['immunization'] = False
G.nodes[37]['target'] = True
G.nodes[38]['immunization'] = False
G.nodes[38]['target'] = True
G.nodes[39]['immunization'] = False
G.nodes[39]['target'] = True
G.nodes[40]['immunization'] = False
G.nodes[40]['target'] = True

G.add_edge(39, 41)
G.add_edge(40, 42)

G.nodes[41]['immunization'] = True
G.nodes[41]['target'] = False
G.nodes[42]['immunization'] = True
G.nodes[42]['target'] = False

G.add_edge(41, 43)
G.add_edge(41, 44)
G.add_edge(43, 45)
G.add_edge(44, 45)

G.nodes[43]['immunization'] = False
G.nodes[43]['target'] = False
G.nodes[44]['immunization'] = False
G.nodes[44]['target'] = False
G.nodes[45]['immunization'] = True
G.nodes[45]['target'] = False

G.add_edge(45, 46)
G.add_edge(42, 47)
G.add_edge(46, 48)
G.add_edge(47, 48)
G.add_edge(14, 46)

G.nodes[46]['immunization'] = False
G.nodes[46]['target'] = True
G.nodes[47]['immunization'] = False
G.nodes[47]['target'] = True
G.nodes[48]['immunization'] = True
G.nodes[48]['target'] = False

drawNetwork2(G, [], 'testing.png')
I = [node for node in G if G.nodes[node]['immunization']]
for node in G:
    G.nodes[node]['size'] = 1
print('---------')
M, dict_M = constructMetaTree(G, I)
drawNetwork2(M, [], 'MetaTree.png')

