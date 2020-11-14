import networkx as nx

# Returns a path of the type I-V-I (I: Immunized, V: Vulnerable)
def DFS_metaTreelen2(G, T, V, N, len):
    T.append(N)
    V[N] = True
    if len == 2:
        return True
    for node in list(G.adj[N]):
        if G.nodes[node]['immunization'] == False:
            if G.nodes[node]['target'] == False and V[node] == False:
                return DFS_metaTreelen2(G, T, V, node, len + 1)
        else:
            if V[node] == False:
                return DFS_metaTreelen2(G, T, V, node, len + 1)
    return False

# Returns a cycle with parent node O with length > 2
def DFS_metaTreeCycle(G, T, V, O, N, len):
    T.append(N)
    aux_T = T[:]
    V[N] = True
    for node in list(G.adj[N]):
        if node == O and len > 1:
            return [T, True]
        elif V[node] == False:
            [T, aux] = DFS_metaTreeCycle(G, T, V, O, node, len + 1)
            if aux:
                return [T, True]
            else:
                T = aux_T
    return [T, False]

# I list of immunized nodes
def constructMetaTree(G, I):
    index = 0
    while(index < len(I)):
        tempt = []
        visited = {item:False for item in G.nodes}
        if DFS_metaTreelen2(G, tempt, visited, I[index],  0):
            for index in range(1, len(tempt)):
                G = nx.contracted_nodes(G, tempt[0], tempt[index], self_loops = False)
                if tempt[index] in I:
                    I.remove(tempt[index])
        else:
            index += 1

    #drawNetwork(G)

    index = 0
    while(index < len(I)):
        tempt = []
        visited = {item:False for item in G.nodes}
        [tempt, aux] = DFS_metaTreeCycle(G, tempt, visited, I[index], I[index],  0)
        if aux:
            for index in range(1, len(tempt)):
                G = nx.contracted_nodes(G, tempt[0], tempt[index], self_loops = False)
                if tempt[index] in I:
                    I.remove(tempt[index])
        else:
            index += 1

    #drawNetwork(G)

    leaf = [x for x in G.nodes if G.degree[x] == 1 and G.nodes[x]['immunization'] == False]
    for item in leaf:
        G = nx.contracted_nodes(G, next(G.neighbors(item)), item, self_loops = False)

    return G
