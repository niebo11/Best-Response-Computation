import networkx as nx
import matplotlib.pyplot as plt
import random

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

def immunize(G, i):
    result = []
    for k in range(0, int(float(10/100*i))):
        n = random.randint(1, i)
        result.append(n)
    return result

def DFS(G, temp, node, visited):
    print(node)
    visited[node] = True

    temp.append(node)

    for neighbor in list(G.adj[node]):
        if visited[neighbor] == False:
            temp = DFS(G, temp, neighbor, visited)

    return temp
    

if __name__ == '__main__':
    n = input('Enter a number: ')
    n = int(n)
    for i in range(2, n):
        try:
            num = random.randint(1, i/2)
            G = nx.connected_caveman_graph(i, num)
            I = immunize(G, i)
            for node in G:
                if node in I:
                    G.nodes[node]['immunization'] = True
                else:
                    G.nodes[node]['immunization'] = False
            
            print(I)
            
            drawNetwork(G)
                    
            visited = [False] * i
            for node in I:
                visite[node] = True
            
            max_T = 1
            for node in G:
                if visited[node] == False:
                    temp = []
                    print('hi')
                    temp = DFS(G, temp, node, visited)
                    print('haiya')
                    if len(temp) > max_T:
                        max_T = len(temp)
            print(max_T)
                    
        except:
            pass
    
