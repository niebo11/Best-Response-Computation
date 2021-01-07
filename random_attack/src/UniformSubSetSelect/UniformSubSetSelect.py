# m number of components (explicitly maximum number of edges)
# n number of nodes we can connect to
# Cu Set of vulnerable connected components
# T_size Size of the target region
# alpha Creation cost of one edge
def uniformSubSetSelect(m, n, Cu, alpha):
    # Matrix of tuples (number of nodes we are connected to, list of components we are connected to)
    M = [[[(0, []) for _ in range(n + 1)] for _ in range(m + 1)] for _ in range(m + 1)]

    for x in range(m + 1):
        for y in range(m + 1):
            for z in range(n + 1):
                if x == 0 or y == 0 or z == 0:
                    M[x][y][z] = (0, [])
                elif z < len(Cu[x - 1]):
                    M[x][y][z] = M[x - 1][y][z]
                else:
                    Cx = len(Cu[x - 1])
                    # Case 1: we want to connect to component x
                    if M[x - 1][y - 1][z - Cx][0] + Cx > M[x - 1][y][z][0]:
                        # Here we need to make a copy of the array M[x-1][y-1][z-Cx][1][:] otherwise we are working
                        # by reference
                        M[x][y][z] = (M[x - 1][y - 1][z - Cx][0] + Cx, M[x - 1][y - 1][z - Cx][1][:])
                        M[x][y][z][1].append(Cu[x - 1])
                    # Case 2: we don't want to
                    else:
                        M[x][y][z] = M[x - 1][y][z]

    k = []
    for z in range(n + 1):
        for j in range(m+1):
            if M[m][j][z][0] == z:
                k.append((m, j, z))
                break
    alpha = []
    for x, y, z in k:
        alpha = 1
    return []