import unittest
from ..searcher import Search


class TestSearch(unittest.TestCase):
    def setUp(self):
        pass

    def test_raises_exception_if_missing_args(self):
        with self.assertRaises(TypeError):
            Search()

        with self.assertRaises(TypeError):
            Search(transition_function=True, data_structure=True, goal_state=True)
