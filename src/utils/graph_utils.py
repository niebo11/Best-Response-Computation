import networkx as nx
from src.PossibleStrategy.MetaTreeConstruct.ComponentsCollapse import DFS_collapse
import matplotlib.pyplot as plt


def dfs_attacked(M, visited, t):
    visited[t] = True
    for NEIGHBOR in list(M.adj[t]):
        if not M.nodes[NEIGHBOR]['immunization'] and not visited[NEIGHBOR]:
            dfs_attacked(M, visited, NEIGHBOR)


def dfs_reachable(M, visited, node):
    result = 1
    visited[node] = True
    for NEIGHBOR in list(M.adj[node]):
        if not visited[NEIGHBOR]:
            result += dfs_reachable(M, visited, NEIGHBOR)
    return result


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
def connectedComponents(G):
    T_size = 0
    max_T = 0

    n = G.number_of_nodes()
    Cu = []
    Ci = []
    visited = [False] * n

    for node in range(n):
        if not visited[node]:
            temp = []
            Immunized = False
            [temp, Immunized] = DFS(G, temp, node, visited, Immunized)

            if not Immunized:
                Cu.append(temp)
                if len(temp) > max_T:
                    T_size = max_T = len(temp)
                elif len(temp) == max_T:
                    T_size += max_T
            else:
                Ci.append(temp)
                [temp_T, temp_count] = Target_region(G, temp, 0)
                if temp_T > max_T:
                    max_T = temp_T
                    T_size = max_T * temp_count
                elif temp_T == max_T:
                    T_size += max_T * temp_count

    return [Cu, Ci, T_size, max_T]


def paintTarget(G, T_size):
    max_T = 0
    visited = [False] * G.number_of_nodes()
    for node in G:
        if not visited[node]:
            if G.nodes[node]["immunization"]:
                visited[node] = True
                G.nodes[node]["target"] = False
            else:
                tempt = []
                DFS_collapse(G, tempt, visited, node, False)
                if len(tempt) == T_size:
                    max_T += T_size
                    for item in tempt:
                        G.nodes[item]["target"] = True
                else:
                    for item in tempt:
                        G.nodes[item]["target"] = False
    return G, max_T


def utility_s(G, T):
    target_objectives = [item for item in G.nodes() if G.nodes[item]['target']]
    result = 1
    for t in target_objectives:
        visited = {item: False for item in G.nodes()}
        dfs_attacked(G, visited, t)
        for node in T:
            if not visited[node]:
                result += dfs_reachable(G, visited, node)
    return result
