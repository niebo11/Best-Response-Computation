import networkx as nx


# Returns a path of the type I-V-I (I: Immunized, V: Vulnerable)
def DFS_metaTree_len2(G, T, V, N, length):
    T.append(N)
    V[N] = True
    if length == 2:
        return True
    for node in list(G.adj[N]):
        if not G.nodes[node]['immunization']:
            if not G.nodes[node]['target'] and not V[node]:
                return DFS_metaTree_len2(G, T, V, node, length + 1)
        else:
            if not V[node]:
                return DFS_metaTree_len2(G, T, V, node, length + 1)
    return False


# Returns a cycle with parent node O with length > 2
def DFS_metaTree_cycle(G, T, V, Origin, N, length):
    T.append(N)
    aux_T = T[:]
    V[N] = True
    # print(T)
    for node in list(G.adj[N]):
        if node == Origin and length > 1:
            return [T, True]
        elif not V[node]:
            [T, aux] = DFS_metaTree_cycle(G, T, V, Origin, node, length + 1)
            if aux:
                return [T, True]
            else:
                T = aux_T
    return [T, False]


# I list of immunized nodes
def constructMetaTree(G, l_I):
    index = 0
    while index < len(l_I):
        tempt = []
        visited = {item: False for item in G.nodes}
        if DFS_metaTree_len2(G, tempt, visited, l_I[index], 0):
            for index in range(1, len(tempt)):
                if tempt[index] in l_I:
                    G.nodes[tempt[0]]['size'] += G.nodes[tempt[index]]['size']
                    G = nx.contracted_nodes(G, tempt[0], tempt[index], self_loops=False)
                    l_I.remove(tempt[index])
        else:
            index += 1

    # drawNetwork(G)

    index = 0
    while index < len(l_I):
        tempt = []
        visited = {item: False for item in G.nodes}
        [tempt, aux] = DFS_metaTree_cycle(G, tempt, visited, l_I[index], l_I[index], 0)
        if aux:
            for index in range(1, len(tempt)):
                if tempt[index] in l_I:
                    G.nodes[tempt[0]]['size'] += G.nodes[tempt[index]]['size']
                    G = nx.contracted_nodes(G, tempt[0], tempt[index], self_loops=False)
                    l_I.remove(tempt[index])
        else:
            index += 1

    leaf = [x for x in G.nodes if G.degree[x] == 1 and not G.nodes[x]['immunization']]
    for item in leaf:
        G.nodes[next(G.neighbors(item))]['size'] += G.nodes[item]['size']
        G = nx.contracted_nodes(G, next(G.neighbors(item)), item, self_loops=False)

    return G
