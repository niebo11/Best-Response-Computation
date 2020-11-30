def profit(M, l, l_d):
    


def RootedMetaTreeSelect(M, rt, leaf, r, alpha, l_d):
    opt = []
    
    for child in list(M.adj[rt]):
        if child != r:
            opt.append(RootedMetaTreeSelect(M, child, rt)
    
    if M.nodes[rt]['immunization'] == False or len(child) == 0:
        return opt
    
    profit = {}
    
    max_profit = -1
    max_l = -1
    
    # ATTENTTION
    for l in leaf:
        p = profit(l)
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
        leverage_dict = leverage(M, neighboor, visited, leverage_dict, level + 1)
    
    return leverage_dict
    

def MetaTreeSelect(M, alpha):
    #Fulles de M
    leaf = [x for x in M.nodes if M.degree[x] == 1]
    for r in leaf:
        visited = [False] * M.number_of_nodes()
        leverage_dict = leverage(M, r, visited, {}, 0)
        aux = leaf[:]
        aux.remove(r)
        result = [r]
        w = next(G.neighbors(item))
        opt[r] = r.append(RootedMetaTreeSelect(M, w, aux, r, leverage_dict, alpha))
