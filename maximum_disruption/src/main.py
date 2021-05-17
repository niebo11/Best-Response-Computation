from bestResponse import bestResponse
from utils.graph_utils import drawNetwork, paintTarget, utility_s, renameGraph
from maximum_disruption.src.PossibleStrategy.MetaTreeConstruct.ComponentsCollapse import DFS_collapse
import networkx as nx


def getSize(G, node, visited):
    visited[node] = True
    result = G.nodes[node]['size']
    for neighbor in G.adj[node]:
        if not visited[neighbor]:
            result += getSize(G, neighbor, visited)
    return result


def socialWelfare(G, attacked):
    result = 0
    visited = [False] * G.number_of_nodes()
    visited[attacked] = True
    for node in G:
        if not visited[node]:
            n = getSize(G, node, visited)
            print(n)
            result += n * (n - 1)
    return result


def collapse_graph(G):
    collapse_dict = {}
    collapseCC = []
    Immunized = []
    visited = [False] * G.number_of_nodes()
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


def initial_utility(G, v, alpha, beta):
    G_ini = G.to_undirected()
    G_ini.remove_nodes_from([node for node in G.nodes if G_ini.nodes[node]['immunization']])
    length_of_vulnerable_region = list(map(len, list(nx.connected_components(G_ini))))
    if len(length_of_vulnerable_region) > 0:
        size_T = max(length_of_vulnerable_region)
    else:
        size_T = 0
    G_ini = G.to_undirected()
    G_ini, max_T, R_t = paintTarget(G_ini, size_T)
    return utility_s(G_ini, v, R_t, max_T) - len(list(G.out_edges(v))) * alpha - G.nodes[v]['immunization'] * beta


if __name__ == '__main__':
    G = nx.read_gpickle("../test/Global test/forest.pickle")
    G.add_node(16)
    G.add_edge(17, 18)
    G.add_node(19)

    G.add_edge(17, 16)
    G.add_edge(16, 19)

    G.nodes[16]['immunization'] = True
    G.nodes[18]['immunization'] = False

    G.nodes[17]['immunization'] = False

    G.nodes[19]['immunization'] = False

    alpha = G.nodes[0]['alpha']
    beta = G.nodes[0]['beta']
    G = G.to_undirected()
    drawNetwork(G)
    G2, I, C_D = collapse_graph(G)
    G3, R_D = renameGraph(G2)
    drawNetwork(G3)
    PostAttack = []
    for node in G3:
        if not G3.nodes[node]['immunization']:
            PostAttack.append((node, socialWelfare(G3, node)))

    print(PostAttack)

    #
    # for i in range(0, G.number_of_nodes()):
    #     print("--------------------------------------")
    #     ini_u = initial_utility(G, i, alpha, beta)
    #     BR = bestResponse(G.copy(), i, alpha, beta)
    #     print("node :", i)
    #     print("initial strategy utility: ", ini_u, "calculated BR utility :", BR[1])
    #     if BR[1] > ini_u:
    #         print(BR[0])
