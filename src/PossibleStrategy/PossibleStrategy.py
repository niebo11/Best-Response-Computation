from MetaTreeConstruct.MetaTreeConstruct import constructMetaTree
from MetaTreeSelect.MetaTreeSelect import MetaTreeSelect
from MetaTreeConstruct.ComponentsCollapse import collapse_graph
from ..utils.graph_utils import renameGraph


def dfs_attacked(M, visited, t):
    visited[t] = True
    for NEIGHBOR in list(M.adj[t]):
        if not M.nodes[NEIGHBOR]['immunization'] and not visited[NEIGHBOR]:
            dfs_attacked(M, visited, NEIGHBOR)


def dfs_reachable(M, visited, node):
    result = 1
    visited[node] = True
    for NEIGHBOR in list(M.adj[node]):
        if not visited[NEIGHBOR]:
            result += dfs_reachable(M, visited, NEIGHBOR)
    return result


# G graph
# C element of the connected component
# T nodes we are connected to
def Utility(G, C, T, target_size):
    visited = {item: False for item in C}
    target_objectives = [item for item in C if G.nodes[item]['target']]
    result = 0
    for t in target_objectives:
        dfs_attacked(G, visited, t)
        for node in T:
            result += dfs_reachable(G, visited, node)
    result = 1 / target_size * result
    return result


def PossibleStrategy(G, CI, Cinc, alpha, target_size, T_size):
    tempt = [item for item in Cinc if CI in CI]
    empty = Utility(G, CI, [] + tempt, alpha, T_size)
    CImm = [item for item in CI if G.nodes[item]['immunization']]
    single_edge = {item: (Utility(G, CI, [item] + tempt, alpha, T_size) - alpha) for item in CImm}
    #TODO change parameter
    [G, C_D, I] = collapse_graph(G, target_size)
    M = constructMetaTree(G, I)
    [M1, mapping] = renameGraph(M)
    opt = MetaTreeSelect(M1, alpha, T_size)
    multiple_edge = {item: (Utility(G, CI, list(item) + tempt, alpha, T_size) - alpha * len(item))
                     for item in opt}

    max_multiple_edge = max(multiple_edge, key=multiple_edge.get)
    max_single_edge = max(single_edge, key=multiple_edge.get)
    if empty > multiple_edge[max_multiple_edge]:
        if empty > single_edge[max_single_edge]:
            return []
        else:
            return [max_single_edge]
    else:
        if multiple_edge[max_multiple_edge] > single_edge[max_single_edge]:
            return max_multiple_edge
        else:
            return [max_single_edge]


