import unittest
from ..containers import Queue


class TestQueue(unittest.TestCase):
    def setUp(self):
        self.queue = Queue()

    def test_respects_fifo(self):
        self.queue.add(1)
        self.queue.add(2)
        self.queue.add(3)
        self.assertEqual(1, self.queue.next())
        self.assertEqual(2, self.queue.next())
        self.assertEqual(3, self.queue.next())

    def test_returns_none_when_empty(self):
        self.queue.add(1)
        self.assertEqual(1, self.queue.next())
        self.assertEqual(None, self.queue.next())
