from maximum_carnage.src.bestResponse import bestResponse
from maximum_carnage.test.utils.utils import randomGraph3
import time
from matplotlib import pyplot as plt
from statistics import mean
import itertools
import networkx as nx
from maximum_carnage.src.utils.graph_utils import initial_utility


if __name__ == '__main__':
    test = True
    iteration = 4
    times = []
    times2 = []
    x = []
    alpha = 8.5
    beta = 10
    while test:
        print(iteration)
        iteration += 1
        x.append(iteration)
        n = iteration
        results = []
        results2 = []
        for j in range(0, 10):
            G = randomGraph3(n, 1/n)
            start = time.time()
            BR = bestResponse(G.copy(), 0, alpha, beta)
            end = time.time()
            results.append((end - start) * 1000.0)

            G2 = G.copy()
            strategies = []
            utilities = []
            utilities2 = []
            aux = list(range(0, G.number_of_nodes()))
            aux.remove(0)
            for L in range(0, int(G.number_of_nodes()/alpha)):
                for subset in itertools.combinations(aux, L):
                    strategies.append(list(subset))
            current_strategy = [(0, k) for k in G.adj[0]]
            G2.remove_edges_from(current_strategy)
            start = time.time()
            for item in strategies:
                G3 = G2.copy()
                new_strategy = [(0, k) for k in item]
                G3.add_edges_from(new_strategy)
                utilities.append(initial_utility(G3, 0, alpha, beta))
            for item in strategies:
                G3 = G2.copy()
                G3.nodes[0]['immunization'] = not G3.nodes[0]['immunization']
                new_strategy = [(0, k) for k in item]
                G3.add_edges_from(new_strategy)
                utilities2.append(initial_utility(G3, 0, alpha, beta))
            max_utility = max(max(utilities), max(utilities2))
            end = time.time()
            results2.append((end - start) * 1000.0)
        times2.append(mean(results2))
        times.append(mean(results))
        if mean(results) > 5000:
            test = False
        if iteration == 20:
            test = False
    plt.plot(x, times, 'black', label='Best Response algorithm')
    plt.plot(x, times2, 'red', label='Brute Force algorithm')

    plt.legend()
    plt.xlabel('Number of players')
    plt.ylabel('Time (milliseconds)')
    plt.show()
