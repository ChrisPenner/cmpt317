import unittest
from ..a1 import _get_possible_movements
from ..problem_generator import Point

nodes_1 = [(0, 0), (1, 0), (0, 1), (1, 1)]

class TestA1(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_possible_movements(self):
        expected = [(1, 0), (0, 1)]
        self.assertItemsEqual(expected, _get_possible_movements(nodes_1, Point(0, 0)))
