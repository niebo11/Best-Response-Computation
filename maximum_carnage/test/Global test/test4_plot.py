from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import linregress

if __name__ == '__main__':
    x = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    times = [
        4.088854789733887, 9.474611282348633, 21.406173706054688, 48.16749095916748, 105.79502582550049,
        233.607816696167,
        507.01653957366943, 1113.70530128479, 2480.5785179138184, 5112.110590934753, 11195.10509967804]
    plt.figure(0)
    log_times = np.log(times)
    plt.semilogy(x, times)
    plt.xlabel('Number of players')
    plt.ylabel('Time in milliseconds')
    plt.title('')
    plt.show()
