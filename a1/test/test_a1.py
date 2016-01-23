import unittest
from ..a1 import _get_possible_movements, transition
from ..problem_generator import Point, State, Package, Driver

from operator import itemgetter

nodes_1 = [(0, 0), (1, 0), (0, 1), (1, 1)]
packages_1 = frozenset([Package(0, Point(1, 1))])
drivers_1 = frozenset([Driver(0, Point(1, 1))])

class TestA1(unittest.TestCase):
    def setUp(self):
        pass

    def test_get_possible_movements(self):
        expected = [(1, 0), (0, 1)]
        self.assertItemsEqual(expected, _get_possible_movements(nodes_1, Point(0, 0)))

    def test_transition(self):
        self.maxDiff = None
        state = State(packages=packages_1, drivers=drivers_1)
        expected = [
            State(
                packages=frozenset([Package(0, Point(1, 1))]),
                drivers=frozenset([Driver(0, Point(1, 0))]),
            ),
            State(
                packages=frozenset([Package(0, Point(1, 1))]),
                drivers=frozenset([Driver(0, Point(0, 1))]),
            ),
            State(
                packages=frozenset([Package(0, Point(0, 1))]),
                drivers=frozenset([Driver(0, Point(0, 1))]),
            ),
            State(
                packages=frozenset([Package(0, Point(1, 0))]),
                drivers=frozenset([Driver(0, Point(1, 0))]),
            ),
        ]
        # Check if values are equal, ignoring costs right now
        # The itemgetter(1) gets only the value, ignoring cost
        self.assertItemsEqual(expected, map(itemgetter(1), transition(nodes_1, state)))
