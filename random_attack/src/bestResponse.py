from utils.graph_utils import connectedComponents, paintTarget, utility_s, DFS_size
from UniformSubSetSelect.UniformSubSetSelect import uniformSubSetSelect
from GreedySelect.GreedySelect import greedySelect
from PossibleStrategy.PossibleStrategy import possibleStrategy
import networkx as nx


# G is a directed graph
# v is the player which we want to compute the best response
def bestResponse(G, v, alpha, beta):
    outEdge = list(G.out_edges(v))
    Cinc = [u for (u, _) in G.in_edges(v)]
    # Remove all the edges player v bought
    for edge in outEdge:
        G.remove_edge(*edge)
    # Compute all the CC and classify them (We will treat G as undirected graph hereinafter)
    G_undirected = G.to_undirected()
    v_size = DFS_size(G_undirected, 0, v, {n: G_undirected.nodes[n]['immunization'] for n in G_undirected.nodes()})
    G_undirected.remove_node(v)
    [Cu, Ci, max_T, T_size] = connectedComponents(G_undirected)
    T_size_Imm = T_size
    if v_size > T_size:
        T_size = max_T = v_size
    Cu_minus_Cinc = []
    for CC in Cu:
        aux = True
        for item in Cinc:
            if item in CC:
                aux = False
        if aux:
            Cu_minus_Cinc.append(CC)
    # First case we don't immunize
    print(Cu_minus_Cinc)
    Au = uniformSubSetSelect(len(Cu_minus_Cinc), sum(map(len, Cu_minus_Cinc)), Cu, alpha)
    Ag = greedySelect(Cu_minus_Cinc, max_T, T_size, alpha)

    utility = []

    G_undirected = G.to_undirected()
    nx.set_node_attributes(G_undirected, {v: False}, 'immunization')
    G1_undirected, max_T = paintTarget(G_undirected, T_size)
    G1_undirected.remove_node(v)
    Sv = possibleStrategy(G1_undirected, Au, False, Ci, Cinc, alpha, max_T, T_size)
    utility.append(1 / max_T * utility_s(G1_undirected, Sv[0]) - len(Sv[0]) * alpha - Sv[1] * beta)

    G_undirected = G.to_undirected()
    nx.set_node_attributes(G_undirected, {v: True}, 'immunization')
    G2_undirected, max_T = paintTarget(G_undirected, T_size_Imm)
    Sg = possibleStrategy(G2_undirected, Ag, True, Ci, Cinc, alpha, max_T, T_size_Imm)
    utility.append(1 / max_T * utility_s(G1_undirected, Sg[0]) - len(Sg[0]) * alpha - Sg[1] * beta)

    print(utility)
    i = utility.index(max(utility))
    if i == 0:
        return Sv, utility[i]
    else:
        return Sg, utility[i]
