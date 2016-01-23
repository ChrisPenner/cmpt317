import unittest
from ..containers import Heap


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.heap = Heap()

    def test_respects_heap_property(self):
        self.heap.add((3, None))
        self.heap.add((2, None))
        self.heap.add((5, None))
        self.heap.add((1, None))
        self.assertEqual((1, None), self.heap.next())
        self.assertEqual((2, None), self.heap.next())
        self.assertEqual((3, None), self.heap.next())
        self.assertEqual((5, None), self.heap.next())

    def test_returns_none_when_empty(self):
        self.heap.add((1, None))
        self.assertEqual((1, None), self.heap.next())
        self.assertEqual(None, self.heap.next())
