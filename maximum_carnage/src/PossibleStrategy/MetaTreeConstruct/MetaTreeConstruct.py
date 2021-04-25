import networkx as nx


# Returns a path of the type I-V-I (I: Immunized, V: Vulnerable)
def DFS_metaTree_len2(G, T, V, N):
    find = False
    T.append(N)
    aux_T = T[:]
    V[N] = True
    if len(T) == 3:
        return T, True
    for node in list(G.adj[N]):
        if not V[node]:
            if G.nodes[node]['immunization']:
                T, find = DFS_metaTree_len2(G, T, V, node)
            elif not G.nodes[node]['target']:
                T, find = DFS_metaTree_len2(G, T, V, node)

        if find:
            break
        else:
            T = aux_T[:]

    return T, find


# Returns a cycle with parent node O with length > 2
def DFS_metaTree_cycle(G, T, V, Origin, N, length):
    T.append(N)
    aux_T = T[:]
    V[N] = True
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
    metaTree_dict = {}
    index = 0

    while index < len(l_I):
        if l_I[index] not in metaTree_dict:
            metaTree_dict[l_I[index]] = l_I[index]
        visited = {item: False for item in G.nodes}
        tempt, find = DFS_metaTree_len2(G, [], visited, l_I[index])
        if find:
            metaTree_dict[tempt[2]] = tempt[0]
            G.nodes[tempt[0]]['size'] += G.nodes[tempt[2]]['size']
            G = nx.contracted_nodes(G, tempt[0], tempt[2], self_loops=False)
            l_I.remove(tempt[2])
        else:
            index += 1

    index = 0
    while index < len(l_I):
        if l_I[index] not in metaTree_dict:
            metaTree_dict[l_I[index]] = l_I[index]
        tempt = []
        visited = {item: False for item in G.nodes}
        [tempt, aux] = DFS_metaTree_cycle(G, tempt, visited, l_I[index], l_I[index], 0)
        if aux:
            for i in range(1, len(tempt)):
                if tempt[i] in l_I:
                    metaTree_dict[tempt[i]] = tempt[0]
                    G.nodes[tempt[0]]['size'] += G.nodes[tempt[i]]['size']
                    G = nx.contracted_nodes(G, tempt[0], tempt[i], self_loops=False)
                    l_I.remove(tempt[i])
        else:
            index += 1

    leaf = [x for x in G.nodes if G.degree[x] == 1 and not G.nodes[x]['immunization']]
    for item in leaf:
        metaTree_dict[item] = next(G.neighbors(item))
        G.nodes[next(G.neighbors(item))]['size'] += G.nodes[item]['size']
        G = nx.contracted_nodes(G, next(G.neighbors(item)), item, self_loops=False)

    return G, metaTree_dict
