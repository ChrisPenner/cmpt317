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

    def __init__(self, heuristic):
        """
        Sets up a minimized Heap with an appropriate interface for Search.
        items should be of form (cost, item)
        """
        self.data = []
        self.heuristic = heuristic
        self.past_states = set()

    def next(self):
        """ Return the next state to try """
        if self.data:
            # Discard the heuristic guess, no longer needed
            estimate, cost_so_far, state = heapq.heappop(self.data)
            return (cost_so_far, state)
        else:
            return None

    def add(self, item):
        """ Add the 'item' to our heap if necessary """
        cost, state = item
        # Don't add previously tried states
        if state in self.past_states:
            return
        self.past_states.add(state)
        heapq.heappush(self.data, (self.heuristic(state) + cost, cost, state))
