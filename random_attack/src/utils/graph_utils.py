import networkx as nx
import matplotlib.pyplot as plt


# Return the number of nodes from a connected component
def DFS_size(G, n, node, visited):
    visited[node] = True
    for neighbor in list(G.adj[node]):
        if not visited[neighbor]:
            n = DFS_size(G, n, neighbor, visited)
    return n + 1


# Return the connected components and whether or not it has a immunized player.
def DFS(G, temp, node, visited, Immunized):
    visited[node] = True

    if not Immunized and G.nodes[node]['immunization']:
        Immunized = True

    temp.append(node)

    for neighbor in list(G.adj[node]):
        if not visited[neighbor]:
            [temp, Immunized] = DFS(G, temp, neighbor, visited, Immunized)

    return [temp, Immunized]


def dfs_reachable(M, Nodes, visited, node):
    result = 1.0
    visited[node] = True
    for NEIGHBOR in list(M.adj[node]):
        if not visited[NEIGHBOR] and NEIGHBOR in Nodes:
            result += dfs_reachable(M, Nodes, visited, NEIGHBOR)
    return result


def dfs_attacked(M, visited, t):
    visited[t] = True
    for NEIGHBOR in list(M.adj[t]):
        if not M.nodes[NEIGHBOR]['immunization'] and not visited[NEIGHBOR]:
            dfs_attacked(M, visited, NEIGHBOR)


def drawNetwork(G):
    color_map = []
    for node in G:
        if G.nodes[node]['immunization']:
            color_map.append('cyan')
        else:
            if 'target' in G.nodes[node] and G.nodes[node]['target']:
                color_map.append('orange')
            else:
                color_map.append('red')
    pos = nx.spring_layout(G, k=0.35, iterations=20)
    nx.draw_networkx(G, pos, node_color=color_map, with_labels=True)
    plt.show()


def renameGraph(G):
    mapping = {}
    index = 0
    for node in G:
        mapping[index] = node
        index += 1
    G = nx.relabel_nodes(G, dict(zip(G, range(G.number_of_nodes()))))
    return [G, mapping]


# Return the size of the maximum target region and the times it appears in the immunized component.
def Target_region(G, Ci, max_T):
    count = 0
    visited = {n: G.nodes[n]['immunization'] for n in Ci}
    for node in Ci:
        if not visited[node]:
            n = DFS_size(G, 0, node, visited)
            if n > 0:
                if n > max_T:
                    max_T = n
                    count = 1
                elif n == max_T:
                    count = count + 1

    return [max_T, count]


# Return the immunized components, vulnerable components, T and t_max from a graph G
def connectedComponents(G, v):
    n = G.number_of_nodes()
    Cu = []
    Ci = []
    visited = [False] * (n + 1)
    visited[v] = True

    for node in range(n):
        if not visited[node]:
            temp = []
            Immunized = False
            [temp, Immunized] = DFS(G, temp, node, visited, Immunized)

            if not Immunized:
                Cu.append(temp)
            else:
                Ci.append(temp)

    return Cu, Ci


def paintTarget(G):
    for node in G:
        G.nodes[node]['target'] = not G.nodes[node]['immunization']
    return G


def utility_s(G, TR, v):
    result = 0
    max_T = len([node for node in G if not G.nodes[node]['immunization']])
    for t in TR:
        visited = {item: False for item in G.nodes()}
        for item in t:
            visited[item] = True
        if not visited[v]:
            result += len(t) / max_T * dfs_reachable(G, G.nodes, visited, v)
    return result
