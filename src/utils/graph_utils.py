import networkx as nx
import matplotlib.pyplot as plt

def drawNetwork(G):
    color_map = []
    for node in G:
        if G.nodes[node]['immunization'] == True:
            color_map.append('cyan')
        else:
            if 'target' in G.nodes[node] and G.nodes[node]['target'] == True:
                color_map.append('orange')
            else:
                color_map.append('red')
    nx.draw_networkx(G, node_color=color_map, with_labels = True)
    plt.show()
    
def renameGraph(G):
    mapping = {}
    index = 0
    for node in G:
        mapping[index] = node
        index += 1
    G = nx.relabel_nodes(G, dict(zip( G, range(G.number_of_nodes()))))
    return [G, mapping]
