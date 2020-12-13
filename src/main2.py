from utils.graph_utils import connectedComponents, DFS_size_target
from SubSetSelect.SubSetSelect import subSetSelect
from GreedySelect.GreedySelect import greedySelect
from PossibleStrategy.PossibleStrategy import possibleStrategy



# G is a directed graph
# v is the player which we want to compute the best response
def bestResponse(G, v, alpha):
    outEdge = list(G.out_edges(v))
    Cinc = [u for (u, _) in G.in_edges(v)]
    print(Cinc)
    # Remove all the edges player v bought
    for edge in outEdge:
        G.remove_edge(*edge)
    # Compute all the CC and classify them (We will treat G as undirected graph hereinafter)
    G_undirected = G.to_undirected()
    v_size = DFS_size_target(G_undirected, 0, v, [False] * G_undirected.number_of_nodes())
    G_undirected.remove_node(v)
    [Cu, Ci, max_T, T_size] = connectedComponents(G_undirected)
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
    [At, Av] = subSetSelect(len(Cu_minus_Cinc), r, Cu, T_size, alpha)
    Ag = greedySelect(Cu_minus_Cinc, max_T, T_size, alpha)
    Pt = possibleStrategy(G, At, False, Ci, Cinc, alpha, max_T + r, T_size)