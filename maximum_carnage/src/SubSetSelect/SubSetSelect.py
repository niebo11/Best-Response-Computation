# Algorithm used to compute choice of nodes in a set of components where all the nodes are vulnerable in case we buy
# immunization

# m number of components in Cu
# r number of vulnerable nodes until the connected component of the player becomes targeted
# Cu set of connected components where all nodes are vulnerable
# alpha cost of buying an edge
def subSetSelect(m, r, Cu, alpha):
    # Matrix of tuples (number of nodes we are connected to, list of components we are connected to)
    M = [[[(0, []) for _ in range(r + 1)] for _ in range(m + 1)] for _ in range(m + 1)]

    # Construction of the matrix M
    for x in range(m + 1):
        for y in range(m + 1):
            for z in range(r + 1):
                if x != 0 and y != 0 and z != 0:
                    Cx = len(Cu[x - 1])
                    if z >= Cx and M[x - 1][y - 1][z - Cx][0] + Cx > M[x - 1][y][z][0]:
                        M[x][y][z] = (M[x - 1][y - 1][z - Cx][0] + Cx, M[x - 1][y - 1][z - Cx][1][:])
                        M[x][y][z][1].append(Cu[x - 1])
                    else:
                        M[x][y][z] = M[x - 1][y][z]

    # Exhaustive search for the combination that maximizes the utility of the player in Cu
    i_at = max([j for j in range(m + 1)], key=lambda l: (M[m][l][r][0] - l*alpha))
    at = M[m][i_at][r][1]

    i_av = max([j for j in range(m + 1)], key=lambda l: (M[m][l][r-1][0] - l*alpha))
    av = M[m][i_av][r-1][1]

    return at, av
