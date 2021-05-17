import networkx as nx
from maximum_carnage.src.SubSetSelect.SubSetSelect import subSetSelect
import unittest
import random as rd


class testSubSetSelect(unittest.TestCase):
    def test_emptyset(self):
        for i in range(2, 5):
            max_T = 1
            k = 5
            P = 1.0 - (max_T / i)
            Cu = [[x] for x in range(1, i + 1)]
            # Case where our elements are all targeted
            At, Av = subSetSelect(len(Cu), i+1, Cu, 0.1)
            self.assertEqual(At, Cu, 'At')
            self.assertEqual(Av, Cu, 'Av')
            At, Av = subSetSelect(len(Cu), i, Cu, 0.1)
            self.assertEqual(At, Cu, 'At2')
            self.assertEqual(Av, Cu[:-1], 'Av2')


if __name__ == '__main__':
    unittest.main()
