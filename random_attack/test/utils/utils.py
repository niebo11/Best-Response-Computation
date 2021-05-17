import networkx as nx
from networkx.drawing.nx_agraph import to_agraph
import random as rd


def graphFromList(L):
    G = nx.DiGraph()
    for CC in L:
        first = True
        for item in CC:
            G.add_node(item)
            G.nodes[item]['immunization'] = False
            if first:
                first = False
                previousNode = item
            else:
                G.add_edge(previousNode, item)
                previousNode = item
    return G


def drawNetwork(G, bought, name):
    G.graph['node'] = {'shape': 'circle'}
    G.add_nodes_from(bought, style='filled', fillcolor='lawngreen')
    G.add_nodes_from([node for node in G.nodes if node not in bought and not G.nodes[node]['immunization']],
                     style='filled', fillcolor='darkred')
    G.add_nodes_from([node for node in G.nodes if node not in bought and G.nodes[node]['immunization']],
                     style='filled', fillcolor='aqua')
    for node in G:
        G.add_nodes_from([node], label=('size: ' + str(G.nodes[node]['size'])))

    A = to_agraph(G)
    A.layout('neato')
    A.draw(name)


def translate(L, C_D, R_D):
    reverse_R_D = {v: k for k, v in R_D.items()}
    result = []
    for item in L:
        result.append(reverse_R_D[C_D[item[0]]])
    return result


def DFS_collapse(G, T, V, N, Imm):
    V[N] = True
    T.append(N)
    for node in list(G.adj[N]):
        if G.nodes[node]['immunization'] == Imm and not V[node]:
            T = DFS_collapse(G, T, V, node, Imm)
    return T


def collapse_graph(G):
    collapse_dict = {}
    collapseCC = []
    Immunized = []
    visited = {node: False for node in G.nodes}
    for node in G:
        if not visited[node]:
            tempt = []
            collapseCC.append(DFS_collapse(G, tempt, visited, node, G.nodes[node]['immunization']))
    for item in collapseCC:
        collapse_dict[item[0]] = item[0]
        G.nodes[item[0]]['size'] = 1
        # We collapse the set of nodes
        if len(item) > 1:
            for index in range(1, len(item)):
                collapse_dict[item[index]] = item[0]
                G.nodes[item[0]]['size'] += 1
                # collapse(G, item[0], item[index], collapse_dict)
                G = nx.contracted_nodes(G, item[0], item[index], self_loops=False)
    return G, Immunized, collapse_dict


def renameGraph(G):
    mapping = {}
    index = 0
    for node in G:
        mapping[index] = node
        index += 1
    G = nx.relabel_nodes(G, dict(zip(G, range(G.number_of_nodes()))))
    return G, mapping


def constructCu():
    max_T = int(input('Introduce maximum size of a region: '))
    n = int(input('Introduce number of connected components: '))
    Cu = []
    k = 0
    for i in range(n):
        tempt = rd.randint(1, max_T)
        Cu.append(list(map(lambda x: x + k, list(range(1, tempt + 1)))))
        k += tempt

    return k + 1, Cu
