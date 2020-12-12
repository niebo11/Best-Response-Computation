import networkx as nx
import matplotlib.pyplot as plt


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


def DFS_size_target(G, n, node, visited):
    print(node)
    visited[node] = True
    for NEIGHBOR in list(G.adj[node]):
        if not visited[NEIGHBOR] and not G.nodes[NEIGHBOR]['immunization']:
            n = DFS_size(G, n, NEIGHBOR, visited)
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
