import networkx as nx


# G network
# T temporal array with visited nodes
# V boolean array of visited nodes
# N actual node
# I Type of set we are working with (Immunized or not)
# DFS to search the maximally region in a component C
def DFS_collapse(G, T, V, N, Imm):
    V[N] = True
    T.append(N)
    for node in list(G.adj[N]):
        if G.nodes[node]['immunization'] == Imm and not V[node]:
            T = DFS_collapse(G, T, V, node, Imm)
    return T


# G network
# max_T size of a target region
# return the network collapsed + the set of immunized regions.
def collapse_graph(G, max_T):
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
        # We check if the collapsing set is targeted or not.
        if not G.nodes[item[0]]['immunization']:
            if len(item) == max_T:
                G.nodes[item[0]]['target'] = True
            else:
                G.nodes[item[0]]['target'] = False
        else:
            Immunized.append(item[0])

        G.nodes[item[0]]['size'] = 1
        # We collapse the set of nodes
        if len(item) > 1:
            for index in range(1, len(item)):
                collapse_dict[item[index]] = item[0]
                G.nodes[item[0]]['size'] += 1
                # collapse(G, item[0], item[index], collapse_dict)
                G = nx.contracted_nodes(G, item[0], item[index], self_loops=False)
    return G, Immunized, collapse_dict
