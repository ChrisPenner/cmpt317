import Map as m
from random import randint
from collections import namedtuple

Package = namedtuple('Package', ['number', 'x', 'y'])
Destination = namedtuple('Destination', ['number', 'x', 'y'])
Garage = namedtuple('Garage', ['x', 'y'])
Driver = namedtuple('Driver', ['number', 'x', 'y'])
NKP = namedtuple('NKP', ['grid', 'packages', 'destinations', 'drivers', 'garage', 'start_state', 'goal_state'])
State = namedtuple('State', ['packages', 'drivers'])

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

    for i in xrange(k):
        packages.add(Package(i, randint(0, size - 1), randint(0, size - 1)))
        destinations.add(Destination(i, randint(0, size - 1), randint(0, size - 1)))

    for i in xrange(n):
        drivers.add(Driver(i, randint(0, size - 1), randint(0, size - 1)))

    garage = Garage(randint(0, size - 1), randint(0, size - 1))

    start_state = State(
        packages=packages,
        drivers=drivers,
    )

    goal_state = State(
        packages=set(Package(*d) for d in destinations),
        drivers=set(Driver(i, garage.x, garage.y) for i in xrange(n)),
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
