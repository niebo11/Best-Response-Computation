import operator

def profit(M, l, rt, parent, l_d, profit, t_r, STsize):
    result += M.nodes[parent]['size']*STsize(l)/t_r
    for child in list(M.adj[rt]):
        if l_d[child] > l_d[rt]:
            for child2 in list(M.adj[child]):
                if l_d[child2] > l_d[child]:
                    result += profit[child2][rt]
    profit[rt][l] = result
    return result

def RootedMetaTreeSelect(M, rt, r, alpha, l_d, STsize, profit, t_r):
    opt = []
    
    for child in list(M.adj[rt]):
        if child != r:
            opt.append(RootedMetaTreeSelect(M, child, rt, alpha, l_d, STsize, profit, t_r))
    
    if M.nodes[rt]['immunization'] == False or len(opt) == 0:
        return opt
    
    profit = {}
    
    max_profit = -1
    max_l = -1
    
    # ATTENTTION
    for l in leaf:
        p = profit(M, l, rt, r, l_d, profit, t_r, STsize)
        if p > max_profit:
            max_profit = p
            max_l = l
    
    if max_profit > alpha:
        opt.append(max_l)
        
    return opt
    
def leverage(M, r, visited, leverage_dict, level):
    visited[r] = True
    leverage_dict[r] = level
    
    for neighboor in list(M.adj[r]):
        if visited[neighboor] == False:
            leverage_dict = leverage(M, neighboor, visited, leverage_dict, level + 1)
            
    return leverage_dict
    
def SubTreeSize(M, leaf, Immunized, l_d):
    maxLevel = max(l_d.items(), key=operator.itemgetter(1))[0]
    result = {item:0 for item in M.nodes()}
    sort_i = dict(sorted(l_d.items(), key=lambda item: item[1], reverse = True))
    for item in sort_i:
        if l_d[item] == maxLevel:
            result[item] = M.nodes[item]['size']
        else:
            result[item] = M.nodes[item]['size']
            for child in list(M.adj[item]):
                if l_d[child] > l_d[item]:
                    result[item] += result[child]
    return result
            

def MetaTreeSelect(M, alpha, target_region):
    #Fulles de M
    leaf = [x for x in M.nodes if M.degree[x] == 1]
    n = len(leaf)
    Immunized  = [x for x in M.nodes if M.nodes[x]['immunization'] == True]
    profit = {Immunized[i] : {leaf[item]:0 for item in range(0, len(leaf))} for i in range(0, len(Immunized))}
    for r1 in leaf:
        for r2 in leaf:
            if r1 == r2:
                profit[r1][r1] = M.nodes[r1]['size']
            else:
                profit[r1][r2] = 0
                
    for r in leaf:
        visited = [False] * M.number_of_nodes()
        leverage_dict = leverage(M, r, visited, {}, 0)
        STsize = SubTreeSize(M, leaf, Immunized, leverage_dict)
        result = [r]
        w = next(M.neighbors(r))
        opt[r] = result.append(RootedMetaTreeSelect(M, w, r, alpha, leverage_dict, profit, STsize, target_region))
