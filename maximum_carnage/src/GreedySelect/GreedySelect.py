# Cu Set of vulnerable connected components
# max_T total number of nodes being targeted
# T_size Size of the target region
# alpha Creation cost of one edge


# Cu Set of vulnerable connected components
# max_T total number of nodes being targeted
# T_size Size of the target region
# alpha Creation cost of one edge


def greedySelect(Cu, max_T, T_size, alpha):
    if (1 - (T_size / max_T)) * T_size > alpha:
        return [x for x in Cu if len(x) > alpha]
    else:
        return [x for x in Cu if T_size > len(x) > alpha]
