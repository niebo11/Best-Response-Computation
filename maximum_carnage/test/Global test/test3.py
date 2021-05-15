from maximum_carnage.src.bestResponse import bestResponse
from maximum_carnage.test.utils.utils import randomGraph3
import time
from matplotlib import pyplot as plt
from statistics import mean


if __name__ == '__main__':
    test = True
    iteration = 4
    times = []
    x = []
    alpha = 0.5
    beta = 5
    while test:
        print(iteration)
        iteration += 1
        x.append(iteration)
        n = iteration
        results = []
        for j in range(0, 20):
            G = randomGraph3(n, 0.05)
            start = time.time()
            BR = bestResponse(G.copy(), 0, alpha, beta)
            end = time.time()
            results.append((end - start) * 1000.0)
        times.append(mean(results))
        if mean(results) > 10000:
            test = False
        if iteration == 300:
            test = False
    plt.plot(x, times)
    print(x)
    print(times)
    plt.xlabel('Number of players')
    plt.ylabel('Time (milliseconds)')
    plt.show()
