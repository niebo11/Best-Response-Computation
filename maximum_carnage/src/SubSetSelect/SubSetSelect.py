# m number of components (explicitly maximum number of edges)
# n number of nodes we can connect to
# Cu Set of vulnerable connected components
# T_size Size of the target region
# alpha Creation cost of one edge
def subSetSelect(m, n, Cu, alpha):
    # Matrix of tuples (number of nodes we are connected to, list of components we are connected to)
    M = [[[(0, []) for _ in range(n + 1)] for _ in range(m + 1)] for _ in range(m + 1)]

    for x in range(m + 1):
        for y in range(m + 1):
            for z in range(n + 1):
                if x != 0 and y != 0 and z != 0:
                    Cx = len(Cu[x - 1])
                    if z >= Cx and M[x - 1][y - 1][z - Cx][0] + Cx > M[x - 1][y][z][0]:
                        M[x][y][z] = (M[x - 1][y - 1][z - Cx][0] + Cx, M[x - 1][y - 1][z - Cx][1][:])
                        M[x][y][z][1].append(Cu[x - 1])
                    else:
                        M[x][y][z] = M[x - 1][y][z]

    i_at = max([j for j in range(m + 1)], key=lambda l: (M[m][l][n][0] - l*alpha))
    at = M[m][i_at][n][1]

    i_av = max([j for j in range(m + 1)], key=lambda l: (M[m][l][n-1][0] - l*alpha))
    av = M[m][i_av][n-1][1]

    return [at, av]
