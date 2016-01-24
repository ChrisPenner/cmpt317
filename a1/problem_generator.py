import Map as m
import random
from collections import namedtuple
from functools import partial

Point = namedtuple('Point', ['x', 'y'])
NKP = namedtuple('NKP', ['graph', 'packages', 'destinations', 'drivers', 'garage', 'start_state', 'goal_state'])
State = namedtuple('State', ['packages', 'drivers'])

def get_problem(size, n, k, p):
    """
    :size: The size of the grid will be size x size
    :n: the number of drivers
    :k: the number of packages
    :p: the carrying capacity of each driver
    """
    graph = m.makeMap(size, size, 0) # width, height, gap frequency
    packages = {}
    destinations = {}
    drivers = {}

    # Random point generator (within bounds)
    random_point = partial(random.choice, graph.nodes())

    # Assign packages and their destinations randomly
    for i in xrange(k):
        packages[i] = random_point()
        destinations[i] = random_point()

    garage = random_point()
    # All drivers start at the garage
    for i in xrange(n):
        drivers[i] = garage

    start_state = State(
        packages=packages.copy(),
        drivers=drivers.copy(),
    )

    goal_state = State(
        # Each package's end state is just their destinations
        packages=destinations.copy(),
        drivers={ k:garage for k in drivers.iterkeys()}
    )

    return NKP(
        graph=graph,
        packages=packages,
        destinations=destinations,
        drivers=drivers,
        garage=garage,
        start_state=start_state,
        goal_state=goal_state,
    )
