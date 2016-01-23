from collections import deque
import heapq


class Container(object):
    """
    Basis for a container
    """

    def __init__(self):
        pass

    def next(self, *args, **kwargs):
        raise NotImplementedError("'next' is not implemented")

    def add(self, *args, **kwargs):
        raise NotImplementedError("'add' is not implemented")

    def extend(self, iterable):
        for v in iterable:
            self.add(v)

class Queue(Container):
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

class Stack(Container):
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

    def add(self, item):
        self.data.append(item)

class Heap(Container):
    """
    A basic priority heap datastructure.
    """

    def __init__(self):
        """
        Sets up a minimized Heap with an appropriate interface for Search.
        items should be of form (cost, item)
        """
        self.data = []

    def next(self):
        if self.data:
            return heapq.heappop(self.data)
        else:
            return None

    def add(self, item):
        heapq.heappush(self.data, item)
