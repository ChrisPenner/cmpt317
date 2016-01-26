import unittest
from ..h4 import Area

class TestArea(unittest.TestCase):
    def setUp(self):
        pass

    def test_direction(self):
        a1 = Area((0,0), (1, 1))
        self.assertEqual(a1.horizontal, Area.EAST)
        self.assertEqual(a1.vertical, Area.SOUTH)
        a2 = Area((1,1), (0, 0))
        self.assertEqual(a2.horizontal, Area.WEST)
        self.assertEqual(a2.vertical, Area.NORTH)

    def test_coalesce_when_directions_dont_match(self):
        a1 = Area((0,0), (1, 1))
        a2 = Area((1,1), (0, 0))
        self.assertItemsEqual(a1.coalesce(a2), [a1, a2])
        self.assertItemsEqual(a2.coalesce(a1), [a2, a1])

    def test_coalesce_when_directions_match(self):
        a1 = Area((0,0), (1, 1))
        a2 = Area((0,0), (1, 1))
        self.assertEqual(a1.coalesce(a2)[0], a1)
        self.assertEqual(a2.coalesce(a1)[0], a1)
