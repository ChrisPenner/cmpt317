import unittest
from ..searcher import Searcher


class TestSearch(unittest.TestCase):
    def setUp(self):
        pass

    def test_raises_exception_if_missing_args(self):
        with self.assertRaises(TypeError):
            Searcher()

        with self.assertRaises(TypeError):
            Searcher(transition_function=True, data_structure=True, goal_state=True)
