import networkx as nx
# Innecesary function? Collapse node j into i
def collapse(G, i, j, collapse_dict):
    edges = [item for item in G.adj[j] if item not in G.adj[i]]
    for edge in edges:
        if edge != i:
            G.add_edge(i, edge)
    G.remove_node(j)
    if i in collapse_dict:
        collapse_dict[i].append(j)
    else:
        collapse_dict[i] = [j]

# G network
# T temporal array with visited nodes
# V boolean aray of visited nodes
# N actual node
# I Type of set we are working with (Immunized or not)
def DFS_collapse(G, T, V, N, I):
    V[N] = True

    T.append(N)

    for node in list(G.adj[N]):
        if G.nodes[node]['immunization'] == I and V[node] == False:
            T = DFS_collapse(G, T, V, node, I)

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
        if visited[node] == False:
            tempt = []
            collapseCC.append(DFS_collapse(G, tempt, visited, node, G.nodes[node]['immunization']))
    for item in collapseCC:
        # We check if the collapsing set is targeted or not.
        if G.nodes[item[0]]['immunization'] == False:
            if len(item) == max_T:
                G.nodes[item[0]]['target'] = True
            else:
                G.nodes[item[0]]['target'] = False
        else:
            Immunized.append(item[0])

        # We collapse the set of nodes
        if len(item) > 1:
            for index in range(1, len(item)):
                # collapse(G, item[0], item[index], collapse_dict)
                G = nx.contracted_nodes(G, item[0], item[index], self_loops = False)
    return [G, collapse_dict, Immunized]

