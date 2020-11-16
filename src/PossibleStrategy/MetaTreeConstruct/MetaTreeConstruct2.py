import networkx as nx

def cutVertexDFS(G, N, V, CV, P, low, disc, time):
    children = 0
    V[N] = True
    
    disc[N] = time
    low[N] = time
    
    for node in G.adj[N]:
        if V[node] == False:
            P[node] = N
            children += 1
            time = cutVertexDFS(G, node, V, CV, P, low, disc, time + 1)
            
            low[N] = min(low[N], low[node])
            
            if P[N] == -1 and children > 1:
                CV[N] = True
                
            if P[N] != -1 and low[node] >= disc[N]:
                CV[N] = True
        
        elif node!= P[N]:
            low[N]= min(low[N], disc[node])
            
    return time
            
            
def cutVertex(G):
    n = G.number_of_nodes()
    visited = [False] * n
    disc = [float("Inf")] * n
    low = [float("Inf")] * n
    parent = [-1] * n
    CV = [False] * n
    time = 0
    
    for node in G:
        if visited[node] == False:
            cutVertexDFS(G, node, visited, CV, parent, low, disc, time)
    return CV

def constructMetaTree(G):
    
    CV = cutVertex(G)
    
    CVTarget = []
    
    for index, value in enumerate(CV):
        if value == True:
            if G.nodes[index]['immunization'] == False and G.nodes[index]['target'] == True:
                print(index)
    
