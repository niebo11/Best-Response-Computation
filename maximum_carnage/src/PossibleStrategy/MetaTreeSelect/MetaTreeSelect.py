import networkx as nx


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


def SubTreeNodes(M, tempt, rt, r):
    tempt.append(rt)
    for NEIGHBOR in list(M.adj[rt]):
        if NEIGHBOR != r:
            SubTreeNodes(M, tempt, NEIGHBOR, rt)
    return


# M is the graph
# rt is the actual vertex
# r = p(rt)
def RootedMetaTreeSelect(M, rt, r, alpha, l_d, sub_tree_size, PROFIT, t_r, leaf, nodes):
    opt = []
    for child in list(M.adj[rt]):
        if child != r:
            subTreeNodes = []
            SubTreeNodes(M, subTreeNodes, child, rt)
            opt = opt + RootedMetaTreeSelect(M, child, rt, alpha, l_d, sub_tree_size, PROFIT,
                                             t_r, leaf, subTreeNodes)

    if not (M.nodes[rt]['immunization']) or len(opt) != 0:
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


def leverage(M, r, visited, leverage_dict, level):
    visited[r] = True
    leverage_dict[r] = level

    for neighbor in list(M.adj[r]):
        if not visited[neighbor]:
            leverage_dict = leverage(M, neighbor, visited, leverage_dict, level + 1)

    return leverage_dict


# TODO review
def SubTreeSize(M, sub_tree_sizes, leaf, l_d):
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
                if l_d[CHILD] > l_d[aux]:
                    sub_tree_sizes[item][aux] += sub_tree_sizes[CHILD][item]
            # If the parent was one of its other nodes then we have an easy approach by using the total size of the tree
            for NEIGHBOR in list(M.adj[item]):
                if NEIGHBOR != aux:
                    sub_tree_sizes[item][NEIGHBOR] = total_size - sub_tree_sizes[NEIGHBOR][item]


def MetaTreeSelect(M, alpha, target_region):
    # Fulles de M
    leaf = [x for x in M.nodes if M.degree[x] == 1]
    opt = []
    sub_tree_sizes = [{} for _ in M.nodes]
    # For each immunized node it represents the profit respect to its leaf
    PROFIT = {}
    first_time = True
    for r in leaf:
        leverage_dict = leverage(M, r, visited, {}, 0)
        if first_time:
            SubTreeSize(M, sub_tree_sizes, leaf, leverage_dict)
            first_time = False
        w = next(M.neighbors(r))
        PROFIT = {item: {item: M.nodes[next(M.neighbors(item))]['size'] *
                               sub_tree_sizes[item][next(M.neighbors(item))] / target_region} for item in leaf}
        visited = [False] * M.number_of_nodes()
        aux = set([r] + RootedMetaTreeSelect(M, w, r, alpha, leverage_dict, sub_tree_sizes, PROFIT,
                                             target_region, leaf, M.nodes))
        if aux not in opt:
            opt.append(aux)
    return opt
