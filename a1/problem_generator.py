import Map as m
import random
from collections import namedtuple
from functools import partial

Point = namedtuple('Point', ['x', 'y'])
NKP = namedtuple('NKP', ['grid', 'packages', 'destinations', 'drivers', 'garage', 'start_state', 'goal_state'])
State = namedtuple('State', ['packages', 'drivers'])

def _get_random_point(grid):
    return Point(*random.choice(grid.nodes()))

def get_problem(size, n, k, p):
    """
    :size: The size of the grid will be size x size
    :n: the number of drivers
    :k: the number of packages
    :p: the carrying capacity of each driver
    """
    grid = m.makeMap(size, size, 0.1) # width, height, gap frequency
    packages = {}
    destinations = {}
    drivers = {}
    rp = partial(_get_random_point, grid)

    for i in xrange(k):
        packages[i] = rp()
        destinations[i] = rp()

    garage = rp()
    for i in xrange(n):
        drivers[i] = garage

    start_state = State(
        packages=packages.copy(),
        drivers=drivers.copy(),
    )

    goal_state = State(
        # Package end state is just destinations
        packages=destinations.copy(),
        drivers={ k:garage for k in drivers.iterkeys()}
    )

    return NKP(
        grid,
        packages,
        destinations,
        drivers,
        garage,
        start_state,
        goal_state
    )