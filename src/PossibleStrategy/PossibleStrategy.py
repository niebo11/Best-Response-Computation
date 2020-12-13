from .MetaTreeConstruct.ComponentsCollapse import collapse_graph
from .MetaTreeConstruct.MetaTreeConstruct import constructMetaTree
from .MetaTreeSelect.MetaTreeSelect import MetaTreeSelect
from src.utils.graph_utils import drawNetwork, renameGraph


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
# TODO VISITED IS NOT FINE
def Utility(G, C, T, max_T):
    visited = {item: False for item in C}
    target_objectives = [item for item in C if G.nodes[item]['target']]
    result = 0
    for t in target_objectives:
        dfs_attacked(G, visited, t)
        for node in T:
            result += dfs_reachable(G, visited, node)
    result += 1 / max_T * ((max_T - len(target_objectives)) * len(C))
    return result


def possibleStrategy(G, A, I, Ci, Cinc, alpha, max_T, T_size):
    M = []
    for C in A:
        M.append(C[0])
    B = []
    for C in Ci:
        B += partnerSetSelect(G.subgraph(C), C, Cinc, alpha, max_T, T_size)
    return M + B, I


def partnerSetSelect(G, CI, Cinc, alpha, max_T, T_size):
    tempt = [item for item in Cinc if CI in CI]
    empty = Utility(G, CI, [] + tempt, max_T)
    CImm = [item for item in CI if G.nodes[item]['immunization']]
    single_edge = {item: (Utility(G, CI, [item] + tempt, max_T) - alpha) for item in CImm}
    max_single_edge = max(single_edge, key=single_edge.get)
    # TODO change parameter
    if len(CImm) > 1:
        [G, mappingG] = renameGraph(G)
        [G1, C_D, I] = collapse_graph(G, T_size)
        if len([item for item in G1.nodes if G1.nodes[item]['immunization']]) > 1:
            M = constructMetaTree(G1, I)
            [M1, mappingM] = renameGraph(M)
            if len([item for item in M1.nodes if M1.nodes[item]['immunization']]) > 1:
                opt = MetaTreeSelect(M1, alpha, T_size)
                multiple_edge = {item: (Utility(G, CI, list(item) + tempt, max_T) - alpha * len(item))
                                 for item in opt}

                max_multiple_edge = max(multiple_edge, key=multiple_edge.get)
                if empty > multiple_edge[max_multiple_edge]:
                    if empty > single_edge[max_single_edge]:
                        return []
                    else:
                        return [max_single_edge]
                else:
                    if multiple_edge[max_multiple_edge] > single_edge[max_single_edge]:
                        return [mappingG[mappingM[item]] for item in max_multiple_edge]
                    else:
                        return [max_single_edge]
    if empty > single_edge[max_single_edge]:
        return []
    else:
        return [max_single_edge]
