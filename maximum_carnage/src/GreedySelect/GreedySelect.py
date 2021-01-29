# Cu Set of vulnerable connected components
# max_T total number of nodes being targeted
# T_size Size of the target region
# alpha Creation cost of one edge


# Cu Set of vulnerable connected components
# max_T total number of nodes being targeted
# T_size Size of the target region
# alpha Creation cost of one edge

def greedySelect(Cu, max_T, T_size, alpha):
    A_g = []
    for CC in Cu:
        if (len(CC) == T_size and len(CC)*(1 - (max_T / T_size)) > alpha) or (T_size > len(CC) > alpha):
            A_g.append(CC)
    return A_g
