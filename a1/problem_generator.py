import Map as m
import random
from collections import namedtuple
from functools import partial

Point = namedtuple('Point', ['x', 'y'])
NKP = namedtuple('NKP', ['graph', 'garage', 'capacity', 'start_state', 'goal_state'])
State = namedtuple('State', ['packages', 'drivers'])

def get_problem(size, num_drivers, num_packages, capacity, seed=None):
    """
    :size: The size of the grid will be size x size
    :num_drivers: the number of drivers
    :num_packages: the number of packages
    :capacity: the carrying capacity of each driver
    """
    random.seed(seed)
    graph = m.makeMap(size, size, 0.0) # width, height, gap frequency
    packages = {}
    destinations = {}
    drivers = {}

    # Random point generator (within bounds)
    random_point = partial(random.choice, graph.nodes())

    # Assign packages and their destinations randomly
    for i in xrange(num_packages):
        packages[i] = random_point()
        destinations[i] = random_point()

    garage = random_point()
    # All drivers start at the garage
    for i in xrange(num_drivers):
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
        garage=garage,
        capacity=capacity,
        start_state=start_state,
        goal_state=goal_state,
    )
