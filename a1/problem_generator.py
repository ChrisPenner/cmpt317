import Map as m
import random
from collections import namedtuple
from functools import partial

Point = namedtuple('Point', ['x', 'y'])
NKP = namedtuple('NKP', ['graph', 'garage', 'capacity', 'start_state', 'goal_state'])
State = namedtuple('State', ['packages', 'drivers'])

def repr_nkp(nkp):
    s = "NKP:\n"
    s += 'Garage: ' + repr(nkp.garage) + '\n'
    s += 'start packages: ' + repr(nkp.start_state.packages) + '\n'
    s += 'end packages: ' + repr(nkp.goal_state.packages) + '\n'
    return s
NKP.__repr__ = repr_nkp

def get_problem(size, num_drivers, num_packages, capacity, seed=None):
    """
    :size: The size of the grid will be size x size
    :num_drivers: the number of drivers
    :num_packages: the number of packages
    :capacity: the carrying capacity of each driver
    :seed: Seed the randomness
    """
    # Random point generator (within bounds)
    random_point = lambda: Point(*random.choice(graph.nodes()))

    random.seed(seed)
    graph = m.makeMap(size, size, 0.0) # width, height, gap frequency

    # Randomly assign all packages, destinations, and garage.
    packages = tuple(random_point() for x in range(num_packages))
    destinations = tuple(random_point() for x in range(num_packages))
    garage = random_point()
    # All drivers start on the garage.
    drivers = tuple(garage for _ in range(num_drivers))

    start_state = State(
        packages=packages,
        drivers=drivers
    )

    goal_state = State(
        # Each package's end state is just their destinations
        packages=destinations,
        drivers=drivers
    )

    return NKP(
        graph=graph,
        garage=garage,
        capacity=capacity,
        start_state=start_state,
        goal_state=goal_state,
    )
