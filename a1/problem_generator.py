import Map as m
from random import randint
from collections import namedtuple

Package = namedtuple('Package', ['package_number', 'x', 'y'])
Destination = namedtuple('Destination', ['package_number', 'x', 'y'])
NKP = namedtuple('NKP', ['grid', 'packages', 'destinations'])

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
    for i in xrange(k):
        packages.add(Package(i, randint(0, size - 1), randint(0, size - 1)))
        destinations.add(Destination(i, randint(0, size - 1), randint(0, size - 1)))
    return NKP(grid, packages, destinations)
