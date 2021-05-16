# Algorithm used to compute choice of nodes in a set of components where all the nodes are vulnerable in case we do not
# buy immunization

# Cu is the set of vulnerable nodes
# t_max is the size of a targeted region
# T_size is the number of targeted nodes
# alpha is the cost of buying an edge
def greedySelect(Cu, t_max, T_size, alpha):
    if (1 - (T_size / t_max)) * T_size > alpha:
        return [x for x in Cu if len(x) > alpha]
    else:
        return [x for x in Cu if T_size > len(x) > alpha]
