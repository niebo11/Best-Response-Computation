import networkx as nx
from networkx.drawing.nx_agraph import to_agraph
from maximum_carnage.src.utils.graph_utils import paintTarget
import random as rd


def getTargetRegion(G):
    G_ini = G.to_undirected()
    G_ini.remove_nodes_from([node for node in G.nodes if G_ini.nodes[node]['immunization']])
    CC = list(nx.connected_components(G_ini))
    return max(list(map(len, CC)))


def randomGraph(n):
    G = nx.connected_watts_strogatz_graph(n, 2, 1, seed=rd.randint(1, 10000))
    immunized = rd.sample(range(0, n), int(n / 5.0 + 1))
    dict_immunization = {node: (False if node not in immunized else True) for node in G.nodes()}
    dict_size = {node: 1 for node in G.nodes}
    nx.set_node_attributes(G, dict_immunization, 'immunization')
    nx.set_node_attributes(G, dict_size, 'size')
    t_max = getTargetRegion(G)
    return G, t_max


def randomGraph2(n, target_size):
    dict_size = {}
    first = True
    m = rd.randint(int(n / 2), n)
    G = nx.algorithms.bipartite.generators.random_graph(n, m, p=(1 / n))
    CC = sorted(nx.connected_components(G), key=len, reverse=True)
    largest_cc = max(CC, key=len)
    for i in range(1, 10):
        randomBool = False if 0.5 > rd.random() else True
        item1 = rd.choice([n for n, d in G.nodes(data=True) if d['bipartite'] == randomBool and n in CC[0]])
        item2 = rd.choice([n for n, d in G.nodes(data=True) if d['bipartite'] != randomBool and n in CC[i]])
        largest_cc = largest_cc.union(CC[i])
        G.add_edge(item1, item2)
    G2 = G.subgraph(largest_cc).copy()
    immunized = {n for n, d in G2.nodes(data=True) if d['bipartite'] == 1}
    vulnerable = set(G2) - immunized
    dict_immunization = {node: (False if node in vulnerable else True) for node in G2.nodes()}
    for node in immunized:
        dict_size[node] = rd.randint(1, target_size)
    for node in vulnerable:
        if first or rd.random() < 1 / 5:
            dict_size[node] = target_size
            first = False
        else:
            dict_size[node] = rd.randint(1, target_size - 1)
    dict_target = {node: (True if dict_size[node] == target_size and not dict_immunization[node] else False)
                   for node in G2.nodes()}
    nx.set_node_attributes(G2, dict_immunization, 'immunization')
    nx.set_node_attributes(G2, dict_size, 'size')
    nx.set_node_attributes(G2, dict_target, 'target')
    for n, d in G.nodes(data=True):
        del d['bipartite']

    return G2, immunized


def randomGraph3(n, p):
    G = nx.generators.random_graphs.erdos_renyi_graph(n, p, directed=True)
    immunized = rd.sample(range(0, n), int(n / 4.0 + 1))
    dict_immunization = {node: (False if node not in immunized else True) for node in G.nodes()}
    dict_size = {node: 1 for node in G.nodes}
    nx.set_node_attributes(G, dict_immunization, 'immunization')
    nx.set_node_attributes(G, dict_size, 'size')

    return G


def randomGraph4(n, p):
    G = nx.generators.random_graphs.gnm_random_graph(n, 2*n, directed=True)
    immunized = rd.sample(range(0, n), int(p * n))
    dict_immunization = {node: (False if node not in immunized else True) for node in G.nodes()}
    dict_size = {node: 1 for node in G.nodes}
    nx.set_node_attributes(G, dict_immunization, 'immunization')
    nx.set_node_attributes(G, dict_size, 'size')
    G_aux = G.copy().to_undirected()
    t_max = getTargetRegion(G_aux)
    G, max_T, result = paintTarget(G, t_max)
    return G, t_max


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


def drawNetwork(G, bought, name, profit=False):
    G.graph['overlap'] = False
    G.graph['node'] = {'shape': 'circle'}
    G.add_nodes_from(bought, style='filled', fillcolor='lawngreen')
    G.add_nodes_from([node for node in G.nodes if node not in bought and not G.nodes[node]['immunization']],
                     style='filled', fillcolor='darkred')
    G.add_nodes_from([node for node in G.nodes if node not in bought and G.nodes[node]['immunization']],
                     style='filled', fillcolor='aqua')
    target = nx.get_node_attributes(G, 'target')
    target_node = [key for key, value in target.items() if value is True]
    G.add_nodes_from(target_node, style='filled', fillcolor='orange')
    for node in G:
        if profit:
            G.add_nodes_from([node], label=('ID: ' + str(node) + ' PRFT: '
                                            + str(G.nodes[node]['profit'])))
        else:
            G.add_nodes_from([node], label=('ID:' + str(node) + 'size: ' + str(G.nodes[node]['size'])))

    A = to_agraph(G)
    A.add_subgraph([9, 2, 1], rank='same')
    A.add_subgraph([12, 7, 8], rank='same')
    A.layout('dot')
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
    max_T = int(input('Introduce target region size: '))
    n = int(input('Introduce number of connected components: '))
    T_size = 0
    Cu = []
    k = 0
    for i in range(n):
        tempt = rd.randint(1, max_T)
        Cu.append(list(map(lambda x: x + k, list(range(1, tempt + 1)))))
        k += tempt
        if tempt == max_T:
            T_size += max_T

    if T_size == 0:
        T_size += rd.randint(1, int(n / 5)) * max_T
    else:
        T_size += rd.randint(0, int(n / 5)) * max_T
    return max_T, T_size, Cu
