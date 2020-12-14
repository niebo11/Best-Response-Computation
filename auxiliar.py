import networkx as nx
import random as rnd
import os


def connectedComponent(number_of_nodes, max_nodes, p, Imm):
    CC = nx.DiGraph()
    notAdded = []
    for x in range(number_of_nodes, max_nodes + number_of_nodes):
        CC.add_node(x)
        if Imm:
            if x == number_of_nodes:
                CC.nodes[x]['immunization'] = True
            elif rnd.random() < p:
                CC.nodes[x]['immunization'] = True
            else:
                CC.nodes[x]['immunization'] = False
        else:
            CC.nodes[x]['immunization'] = False
    for x in range(number_of_nodes, max_nodes + number_of_nodes):
        for j in range(number_of_nodes, max_nodes + number_of_nodes):
            if x != j:
                if not CC.has_edge(x, j):
                    if rnd.random() < 0.5:
                        CC.add_edge(x, j)
                    else:
                        notAdded.append((x, j))

    while not nx.is_connected(CC.to_undirected()):
        (x, j) = rnd.choice(notAdded)
        CC.add_edge(x, j)
    return CC


if __name__ == '__main__':
    m = 75
    n = 0
    G = nx.DiGraph()
    while n < m:
        k = rnd.randint(2, 6)
        if k + n > m:
            k = m - n
        M = connectedComponent(n, k, 0.01, (rnd.random() < 0.3))
        G = nx.compose(G, M)
        n = n + k
    G.add_node(m)
    G.nodes[m]['immunization'] = (rnd.random() < 0.3)
    for i in range(0, m):
        if rnd.random() < 0.01:
            G.add_edge(i, m)
        if rnd.random() < 0.05:
            G.add_edge(m, i)

    nx.write_gpickle(G, os.path.dirname(os.path.abspath(__file__)) + '/test/graph3.pickle')
