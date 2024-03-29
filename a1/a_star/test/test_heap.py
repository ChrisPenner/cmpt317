import unittest
from ..containers import Heap


class TestHeap(unittest.TestCase):
    def setUp(self):
        pass

    def test_respects_heap_property_with_heuristic(self):
        h = lambda x: -x
        heap = Heap(heuristic=h)
        heap.add((3, 1))
        heap.add((2, 2))
        heap.add((5, 3))
        heap.add((1, 4))
        self.assertEqual((1, 4), heap.next())
        self.assertEqual((2, 2), heap.next())
        self.assertEqual((3, 1), heap.next())
        self.assertEqual((5, 3), heap.next())

    def test_returns_none_when_empty(self):
        heap = Heap(heuristic=lambda x: x)
        heap.add((1, 5))
        self.assertEqual((1, 5), heap.next())
        self.assertEqual(None, heap.next())
