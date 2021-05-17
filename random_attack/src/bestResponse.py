from utils.graph_utils import connectedComponents, paintTarget, utility_s, DFS_size, drawNetwork
from UniformSubSetSelect.UniformSubSetSelect import uniformSubSetSelect
from GreedySelect.GreedySelect import greedySelect
from PossibleStrategy.PossibleStrategy import possibleStrategy, getTargetRegion
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

    # We do not buy immunization
    G_undirected = G.to_undirected()
    G1_undirected = paintTarget(G_undirected)
    G1_undirected.remove_node(v)
    Su = possibleStrategy(G1_undirected, Au, False, Ci, Cinc, alpha, T_size + 1, currentSize, Targeted=True)

    G1_undirected.add_node(v)
    G1_undirected.nodes[v]['immunization'] = False
    G1_undirected.nodes[v]['target'] = True
    for node in Su[0] + Cinc:
        G1_undirected.add_edge(v, node)
    TR = getTargetRegion(G1_undirected, [node for node in G1_undirected])
    utility.append(utility_s(G1_undirected, TR, v) - len(Su[0]) * alpha - Su[1] * beta)

    # We buy immunization
    G_undirected = G.to_undirected()
    G2_undirected = paintTarget(G_undirected)
    G2_undirected.remove_node(v)
    Sg = possibleStrategy(G2_undirected, Ag, True, Ci, Cinc, alpha, T_size, currentSize, Targeted=False)

    G2_undirected.add_node(v)
    G2_undirected.nodes[v]['immunization'] = True
    G2_undirected.nodes[v]['target'] = False
    for node in Sg[0] + Cinc:
        G2_undirected.add_edge(v, node)
    TR = getTargetRegion(G2_undirected, [node for node in G2_undirected])
    utility.append(utility_s(G1_undirected, TR, v) - len(Sg[0]) * alpha - Sg[1] * beta)

    # empty strategy
    G_undirected = G.to_undirected()
    nx.set_node_attributes(G_undirected, {v: False}, 'immunization')
    G3_undirected = paintTarget(G_undirected)
    utility.append(utility_s(G3_undirected, TR, v))

    i = utility.index(max(utility))
    if i == 0:
        return Su, utility[i]
    elif i == 1:
        return Sg, utility[i]
    else:
        return ([], False), utility[i]
