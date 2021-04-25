import json
import random as rd
import time
import unittest

import matplotlib.pyplot as plt
import numpy as np

from maximum_carnage.src.PossibleStrategy.MetaTreeConstruct.ComponentsCollapse import collapse_graph
from maximum_carnage.src.PossibleStrategy.MetaTreeConstruct.MetaTreeConstruct import constructMetaTree
from maximum_carnage.test.utils.utils import graphFromList, drawNetwork, renameGraph, translate, \
    constructCu, randomGraph, randomGraph2, getTargetRegion


class testGreedySelect(unittest.TestCase):
    @unittest.skip("reason for skipping")
    def test_collapse(self):
        G, t_max = randomGraph(50)
        G2, I, C_D = collapse_graph(G, t_max)
        G2, R_D = renameGraph(G2)
        drawNetwork(G, [], 'test.png')
        drawNetwork(G2, [], 'test_collapse.png')

    @unittest.skip("reason for skipping")
    def test_MetaTreeConstruct(self):
        G, t_max = randomGraph(200)
        G2, I, C_D = collapse_graph(G, t_max)
        G2, R_D = renameGraph(G2)
        inverse_R_D = {value: key for key, value in R_D.items()}
        drawNetwork(G, [], 'test2.png')
        drawNetwork(G2, [], 'test_collapse2.png')
        l_I = [inverse_R_D[item] for item in I]
        M, M_D = constructMetaTree(G2, l_I)
        drawNetwork(M, [], 'test_metaTree.png')

    def test_MetaTreeConstruct2(self):
        target_size = 10
        G, Imm = randomGraph2(500, target_size)
        drawNetwork(G, [], 'test1.png')
        M, M_D = constructMetaTree(G, list(Imm))
        drawNetwork(M, [], 'test1_metaTree.png')


if __name__ == '__main__':
    unittest.main()
