from utils.graph_utils import connectedComponents, paintTarget, utility_s, DFS_size, drawNetwork
from UniformSubSetSelect.UniformSubSetSelect import uniformSubSetSelect
from GreedySelect.GreedySelect import greedySelect
from PossibleStrategy.PossibleStrategy import possibleStrategy
import networkx as nx


def searchCu_minus_Cinc(Cu, Cinc):
    Cu_minus_Cinc = []
    for CC in Cu:
        aux = True
        for item in CC:
            if item in Cinc:
                aux = False
        if aux:
            Cu_minus_Cinc.append(CC)
    return Cu_minus_Cinc


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

    currentSize = DFS_size(G_undirected, 0, v, {n: G_undirected.nodes[n]['immunization'] for n in G_undirected.nodes()})

    G_undirected.remove_node(v)

    Cu, Ci = connectedComponents(G_undirected, v)

    T_size = len([x for x in G_undirected.nodes() if not G_undirected.nodes[x]['immunization']])
    Cu_minus_Cinc = searchCu_minus_Cinc(Cu, Cinc)

    # First case we don't immunize

    Au = uniformSubSetSelect(currentSize, len(Cu_minus_Cinc), T_size, Cu, alpha)
    Ag = greedySelect(Cu_minus_Cinc, T_size, alpha)

    utility = []
    #
    G_undirected = G.to_undirected()
    nx.set_node_attributes(G_undirected, {v: False}, 'immunization')
    G1_undirected = paintTarget(G_undirected)
    G1_undirected.remove_node(v)
    Su = possibleStrategy(G1_undirected, Au, False, Ci, Cinc, alpha, T_size + 1)
    utility.append(1 / (T_size + 1) * utility_s(G1_undirected, Su[0] + Cinc, v) - len(Su[0]) * alpha - Su[1] * beta)
    #
    G_undirected = G.to_undirected()
    nx.set_node_attributes(G_undirected, {v: True}, 'immunization')
    G2_undirected = paintTarget(G_undirected)

    Sg = possibleStrategy(G2_undirected, Ag, True, Ci, Cinc, alpha, T_size)

    drawNetwork(G1_undirected)

    utility.append(1 / T_size * utility_s(G1_undirected, Sg[0] + Cinc, v) - len(Sg[0]) * alpha - Sg[1] * beta)
    #

    i = utility.index(max(utility))
    if i == 0:
        return Su, utility[i]
    else:
        return Sg, utility[i]
