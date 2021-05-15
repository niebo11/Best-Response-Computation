from maximum_carnage.src.bestResponse import bestResponse
from maximum_carnage.test.utils.utils import randomGraph3, randomGraph4
from maximum_carnage.src.PossibleStrategy.MetaTreeConstruct.MetaTreeConstruct import constructMetaTree
from maximum_carnage.src.PossibleStrategy.MetaTreeConstruct.ComponentsCollapse import collapse_graph
import time
from matplotlib import pyplot as plt


if __name__ == '__main__':
    test = True
    iteration = 4
    times = []
    x = []
    alpha = 2
    beta = 2
    G, t_max = randomGraph4(10, 0.5)
    G1, I, dict_collapse = collapse_graph(G, t_max)
    M = constructMetaTree(G1, I)
    print(M.number_of_nodes())
