import unittest
from ..containers import Stack


class TestStack(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()

    def test_respects_lifo(self):
        self.stack.add(1)
        self.stack.add(2)
        self.stack.add(3)
        self.assertEqual(3, next(self.stack))
        self.assertEqual(2, next(self.stack))
        self.assertEqual(1, next(self.stack))

    def test_returns_none_when_empty(self):
        self.stack.add(1)
        self.assertEqual(1, next(self.stack))
        self.assertEqual(None, next(self.stack))
