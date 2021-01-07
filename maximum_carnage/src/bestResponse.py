from utils.graph_utils import connectedComponents, paintTarget, utility_s, DFS_size, drawNetwork
from SubSetSelect.SubSetSelect import subSetSelect
from GreedySelect.GreedySelect import greedySelect
from PossibleStrategy.PossibleStrategy import possibleStrategy
import networkx as nx
import random as rnd


# G is a directed graph
# v is the player which we want to compute the best response
def bestResponse(G_ini, v, alpha, beta):
    G = G_ini.copy()
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
    r = T_size - v_size
    [At, Av] = subSetSelect(len(Cu_minus_Cinc), r, Cu_minus_Cinc, alpha)
    Ag = greedySelect(Cu_minus_Cinc, max_T, T_size, alpha)

    At = [rnd.choice(item) for item in At]
    Av = [rnd.choice(item) for item in Av]
    Ag = [rnd.choice(item) for item in Ag]

    utility = []

    G_undirected = G_ini.to_undirected()
    G_undirected.remove_edges_from(outEdge)
    for item in Av:
        G_undirected.add_edge(v, item)
    nx.set_node_attributes(G_undirected, {v: False}, 'immunization')
    G1_undirected, max_T, R_t = paintTarget(G_undirected, T_size)
    G1_undirected.remove_node(v)
    Sv = possibleStrategy(G1_undirected, Av, False, Ci, Cinc, alpha, max_T, T_size, v)
    G1_undirected.add_node(v)
    G1_undirected.nodes[v]['immunization'] = False
    G1_undirected.nodes[v]['target'] = False
    for node in Sv[0] + Cinc:
        G1_undirected.add_edge(v, node)
    utility.append(utility_s(G1_undirected, v, R_t, max_T) - len(Sv[0]) * alpha - Sv[1] * beta)

    if r > 0:
        G_undirected = G_ini.to_undirected()
        nx.set_node_attributes(G_undirected, {v: False}, 'immunization')
        G_undirected.remove_edges_from(outEdge)
        for item in At:
            G_undirected.add_edge(v, item)
        G1_undirected, max_T, R_t = paintTarget(G_undirected, T_size)
        G1_undirected.remove_node(v)
        St = possibleStrategy(G1_undirected, At, False, Ci, Cinc, alpha, max_T, T_size, v)

        G1_undirected.add_node(v)
        G1_undirected.nodes[v]['immunization'] = False
        G1_undirected.nodes[v]['target'] = True
        for node in St[0] + Cinc:
            G1_undirected.add_edge(v, node)

        utility.append(utility_s(G1_undirected, v, R_t, max_T) - len(St[0]) * alpha - St[1] * beta)

    G_undirected = G_ini.to_undirected()
    nx.set_node_attributes(G_undirected, {v: True}, 'immunization')
    G2_undirected, max_T, R_t = paintTarget(G_undirected, T_size_Imm)
    G2_undirected.remove_node(v)
    Sg = possibleStrategy(G2_undirected, Ag, True, Ci, Cinc, alpha, max_T, T_size_Imm, v)

    G2_undirected.add_node(v)
    G2_undirected.nodes[v]['immunization'] = True
    G2_undirected.nodes[v]['target'] = False
    for node in Sg[0] + Cinc:
        G2_undirected.add_edge(v, node)

    utility.append(utility_s(G2_undirected, v, R_t, max_T) - len(Sg[0]) * alpha - Sg[1] * beta)

    i = utility.index(max(utility))
    if i == 0:
        return Sv, utility[i]
    elif r > 0 and i == 1:
        return St, utility[i]
    else:
        return Sg, utility[i]
