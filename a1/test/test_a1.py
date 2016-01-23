import unittest
from ..a1 import transition, h1
from ..problem_generator import Point, State
import networkx as nx

from operator import itemgetter

# Simple square graph
graph_1 = nx.Graph(data=[
    ((0,0),(0,1)),
    ((0,0),(1,0)),
    ((1,1),(0,1)),
    ((1,1),(1,0)),
])

nodes_1 = [(0, 0), (1, 0), (0, 1), (1, 1)]
packages_1 = { 0: (1, 1) }
packages_2 = { 0: (0, 1) }
packages_3 = { 0: (0, 0) }
drivers_1 = { 0: (1, 1) }
goal_1 = State(packages=packages_1, drivers=drivers_1)
state_1 = State(packages=packages_2, drivers=drivers_1)
state_2 = State(packages=packages_3, drivers=drivers_1)

class TestA1(unittest.TestCase):
    def setUp(self):
        pass

    def test_transition(self):
        self.maxDiff = None
        state = State(packages=packages_1, drivers=drivers_1)
        expected = [
            State(
                packages={0: (1, 1) },
                drivers={0: (1, 0)},
            ),
            State(
                packages={0: (1, 1)},
                drivers={0: (0, 1)},
            ),
            State(
                packages={0: (0, 1)},
                drivers={0: (0, 1)},
            ),
            State(
                packages={0: (1, 0)},
                drivers={0: (1, 0)},
            ),
        ]
        # Check if values are equal, ignoring costs right now
        # The itemgetter(1) gets only the value, ignoring cost
        self.assertItemsEqual(expected, transition(graph_1, state))

    def test_h1_is_0_when_at_goal(self):
        self.assertEqual(0, h1(goal_1, goal_1))

    def test_h1_calculates_proper_distance(self):
        self.assertEqual(1, h1(state_1, goal_1))
        self.assertEqual(2, h1(state_2, goal_1))

