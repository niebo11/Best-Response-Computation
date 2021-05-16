import networkx as nx


# Subroutine that computes the dictionary profit
def profit(M, leaf, rt, parent, l_d, PROFIT, t_r, sub_tree_size):
    result = M.nodes[parent]['size'] * sub_tree_size[rt][parent] / t_r
    for CHILD in list(M.adj[rt]):
        if l_d[CHILD] > l_d[rt]:
            for CHILD2 in list(M.adj[CHILD]):
                if l_d[CHILD2] > l_d[CHILD] and leaf in PROFIT[CHILD2]:
                    result += PROFIT[CHILD2][leaf]

    if rt not in PROFIT:
        PROFIT[rt] = {leaf: result}
    else:
        PROFIT[rt][leaf] = result
    return result


# Returns the child of the node r_t
def SubTreeNodes(M, tempt, rt, r):
    tempt.append(rt)
    for NEIGHBOR in list(M.adj[rt]):
        if NEIGHBOR != r:
            SubTreeNodes(M, tempt, NEIGHBOR, rt)
    return


# Computes the optimal partner for a tree rooted at rt
def RootedMetaTreeSelect(M, rt, r, alpha, Cinc, l_d, sub_tree_size, PROFIT, t_r, leaf, nodes):
    opt = []
    for child in list(M.adj[rt]):
        if child != r:
            subTreeNodes = []
            SubTreeNodes(M, subTreeNodes, child, rt)
            opt = opt + RootedMetaTreeSelect(M, child, rt, alpha, Cinc, l_d, sub_tree_size, PROFIT,
                                             t_r, leaf, subTreeNodes)

    if not (M.nodes[rt]['immunization']) or len(opt) != 0 or rt in Cinc:
        return opt

    max_profit = -1
    max_l = -1

    # ATTENTION
    for L in leaf:
        if L in nodes:
            p = PROFIT[rt][rt] if rt == L else profit(M, L, rt, r, l_d, PROFIT, t_r, sub_tree_size)

            if p > max_profit:
                max_profit = p
                max_l = L
    if max_profit > alpha:
        opt.append(max_l)
    return opt


# Subroutine used to compute the dictionary for a rooted tree
def root_tree(M, r, visited, leverage_dict, level):
    visited[r] = True
    leverage_dict[r] = level

    for neighbor in list(M.adj[r]):
        if not visited[neighbor]:
            leverage_dict = root_tree(M, neighbor, visited, leverage_dict, level + 1)

    return leverage_dict


# Creates the dictionary SBT
def subTreeSize(M, sub_tree_sizes, leaf, l_d):
    total_size = sum(nx.get_node_attributes(M, 'size').values())
    sort_i = dict(sorted(l_d.items(), key=lambda x: x[1], reverse=True))
    for item in sort_i:
        if item in leaf:
            sub_tree_sizes[item][next(M.neighbors(item))] = M.nodes[item]['size']
        else:
            # If everything is correct, each node should have only one parent (Tree definition)
            aux = next((x for x in list(M.adj[item]) if l_d[item] > l_d[x]))
            # We compute the size of the subtree in respect to the tree rooted by l_d
            sub_tree_sizes[item][aux] = M.nodes[item]['size']
            for CHILD in list(M.adj[item]):
                if CHILD != aux:
                    sub_tree_sizes[item][aux] += sub_tree_sizes[CHILD][item]
                    sub_tree_sizes[item][CHILD] = total_size - sub_tree_sizes[CHILD][item]


# Subroutine that return the optimal partner for a MetaTree
def MetaTreeSelect(M, Cinc, alpha, target_region):
    # Fulles de M
    leaf = [x for x in M.nodes if M.degree[x] == 1]
    opt = []
    sub_tree_sizes = [{} for _ in M.nodes]
    # For each immunized node it represents the profit respect to its leaf
    first_time = True
    for r in leaf:
        visited = [False] * M.number_of_nodes()
        leverage_dict = root_tree(M, r, visited, {}, 0)
        if first_time:
            subTreeSize(M, sub_tree_sizes, leaf, leverage_dict)
            first_time = False
        w = next(M.neighbors(r))
        PROFIT = {item: {item: M.nodes[next(M.neighbors(item))]['size'] *
                  sub_tree_sizes[item][next(M.neighbors(item))] / target_region} for item in leaf}
        aux = set([r] + RootedMetaTreeSelect(M, w, r, alpha, Cinc, leverage_dict, sub_tree_sizes, PROFIT,
                                             target_region, leaf, M.nodes))
        if aux not in opt:
            opt.append(aux)
    return opt
