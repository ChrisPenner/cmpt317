import unittest
from ..containers import Stack


class TestStack(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()

    def test_respects_fifo(self):
        self.stack.add(1)
        self.stack.add(2)
        self.stack.add(3)
        self.assertEqual(3, self.stack.next())
        self.assertEqual(2, self.stack.next())
        self.assertEqual(1, self.stack.next())

    def test_returns_none_when_empty(self):
        self.stack.add(1)
        self.assertEqual(1, self.stack.next())
        self.assertEqual(None, self.stack.next())
