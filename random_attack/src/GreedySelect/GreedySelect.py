# Cu Set of vulnerable connected components
# max_T total number of nodes being targeted
# T_size Size of the target region
# alpha Creation cost of one edge

def greedySelect(Cu, T_size, alpha):
    return [x for x in Cu if len(x) * (1-len(x)/T_size) > alpha]
