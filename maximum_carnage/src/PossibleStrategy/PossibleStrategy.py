from .MetaTreeConstruct.ComponentsCollapse import collapse_graph
from .MetaTreeConstruct.MetaTreeConstruct import constructMetaTree
from .MetaTreeSelect.MetaTreeSelect import MetaTreeSelect
import networkx as nx
from maximum_carnage.src.utils.graph_utils import renameGraph, dfs_reachable, dfs_attacked, drawNetwork


def getTargetRegion(G, Components, size_T):
    G_ini = G.to_undirected()
    G_ini.remove_nodes_from([node for node in G.nodes if not G_ini.nodes[node]['target'] and node in Components])
    return list(nx.connected_components(G_ini))


def initial_opt(opt, mappingG, mappingM):
    result = []
    for item in opt:
        tempt = []
        for item2 in item:
            tempt.append(mappingG[mappingM[item2]])
        result.append(tempt)
    return result


# G graph
# C element of the connected component
# T nodes we are connected to
def Utility(G, C, T, targetRegions, max_T, size_T):
    total = 0
    for item in targetRegions:
        visited = {item: False for item in C}
        result = 0
        for elem in item:
            visited[elem] = True
        for elem in T:
            if not visited[elem]:
                result += dfs_reachable(G, C, visited, elem)
        total += size_T / max_T * result
    return total


def possibleStrategy(G, M, Imm, Ci, Cinc, alpha, max_T, T_size, v):
    B = []
    for C in Ci:
        B += partnerSetSelect(G.subgraph(C), C, Cinc, alpha, max_T, T_size)
    return M + B, Imm


def partnerSetSelect(G, CI, Cinc, alpha, max_T, T_size):
    targetRegions = getTargetRegion(G, CI, max_T)
    tempt = [item for item in Cinc if item in CI]
    empty = Utility(G, CI, tempt, targetRegions, max_T, T_size)
    CImm = [item for item in CI if G.nodes[item]['immunization']]
    single_edge = {item: (Utility(G, CI, list(set([item] + tempt)), targetRegions, max_T, T_size) - alpha)
                   for item in CImm if item not in Cinc}
    max_single_edge = max(single_edge, key=single_edge.get)
    # TODO change parameter
    if len(CImm) > 1:
        G1 = G.subgraph(CI)
        G1, mappingG = renameGraph(G1)
        inv_mappingG = {v: k for k, v in mappingG.items()}
        G2, I, collapse_dict = collapse_graph(G1, T_size)
        if len([item for item in G2.nodes if G2.nodes[item]['immunization']]) > 1:
            M, metaTree_dict = constructMetaTree(G2, I)
            [M1, mappingM] = renameGraph(M)
            inv_mappingM = {v: k for k, v in mappingM.items()}
            Cinc_f = list({inv_mappingM[metaTree_dict[collapse_dict[inv_mappingG[item]]]] for item in tempt})

            if len([item for item in M1.nodes if M1.nodes[item]['immunization']]) > 1:
                opt = MetaTreeSelect(M1, Cinc_f, alpha, T_size)
                opt = initial_opt(opt, mappingG, mappingM)

                multiple_edge = {tuple(item): (Utility(G, CI, item + tempt, targetRegions, max_T, T_size) - alpha * len(item))
                                 for item in opt}

                max_multiple_edge = max(multiple_edge, key=multiple_edge.get)

                print(max_multiple_edge)
                print('multiple edge:', multiple_edge[max_multiple_edge])
                print('max single edge:', single_edge[max_single_edge])
                print('empty:', empty)

                if empty > multiple_edge[max_multiple_edge]:
                    if empty > single_edge[max_single_edge]:
                        return []
                    else:
                        return [max_single_edge]
                else:
                    if multiple_edge[max_multiple_edge] > single_edge[max_single_edge]:
                        return [item for item in max_multiple_edge]
                    else:
                        return [max_single_edge]

    if empty > single_edge[max_single_edge]:
        return []
    else:
        return [max_single_edge]
