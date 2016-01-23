from collections import deque

class Queue(object):
    """
    A basic FIFO queue datastructure.
    """

    def __init__(self):
        """
        Sets up a Queue with an appropriate interface for Search.
        """
        self.data = deque()

    def next(self):
        if self.data:
            return self.data.popleft()
        else:
            return None

    def add(self, item):
        self.data.append(item)

class Stack(object):
    """
    A basic LIFO stack datastructure.
    """

    def __init__(self):
        """
        Sets up a Stack with an appropriate interface for Search.
        """
        self.data = []

    def next(self):
        if self.data:
            return self.data.pop()
        else:
            return None
        pass

    def add(self, item):
        self.data.append(item)
