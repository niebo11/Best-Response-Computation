import networkx as nx
import random as rnd
import os


def connectedComponent(n, k, p, I):
    M = nx.DiGraph()
    notAdded = []
    for i in range(n, k + n):
        M.add_node(i)
        if I:
            if i == n:
                M.nodes[i]['immunization'] = True
            elif rnd.random() < p:
                M.nodes[i]['immunization'] = True
            else:
                M.nodes[i]['immunization'] = False
        else:
            M.nodes[i]['immunization'] = False
    for i in range(n, k + n):
        for j in range(n, k + n):
            if i != j:
                if not M.has_edge(i, j):
                    if rnd.random() < 0.5:
                        M.add_edge(i, j)
                    else:
                        notAdded.append((i, j))

    while not nx.is_connected(M.to_undirected()):
        (i, j) = rnd.choice(notAdded)
        M.add_edge(i, j)
    return M


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
