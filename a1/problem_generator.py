import Map as m
import random
from collections import namedtuple
from functools import partial

Point = namedtuple('Point', ['x', 'y'])
Package = namedtuple('Package', ['number', 'point'])
Destination = namedtuple('Destination', ['number', 'point'])
Driver = namedtuple('Driver', ['number', 'point'])
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
    packages = set()
    destinations = set()
    drivers = set()
    rp = partial(_get_random_point, grid)

    for i in xrange(k):
        packages.add(Package(i, rp()))
        destinations.add(Destination(i, rp()))

    for i in xrange(n):
        drivers.add(Driver(i, rp()))

    garage = rp()

    start_state = State(
        packages=packages,
        drivers=drivers,
    )

    goal_state = State(
        packages=set(Package(*d) for d in destinations),
        drivers=set(Driver(i, garage) for i in xrange(n)),
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
