import problem_generator as pg
from problem_generator import State, Point, Driver, Package
from a_star.searcher import Search
from a_star.containers import Heap
from functools import partial

def _get_possible_movements(nodes, p):
    """
    Return all possible nodes that can be reached in the graph given point p
    """
    return [p for p in [Point(p.x - 1, p.y), Point(p.x + 1, p.y),
                        Point(p.x, p.y - 1), Point(p.x, p.y + 1)]
            if p in nodes]

def transition(nodes, state):
    """
    Returns an iterable of all possible next states and the cost to move there
    of the form (cost, next_state)
"""
    possible_moves = partial(_get_possible_movements, nodes)
    for d in state.drivers:
        # Get a set of all other drivers but the current one
        other_drivers = frozenset(state.drivers) - {d}
        for p in possible_moves(d.point):
            # Create a new driver with the new position
            new_driver = Driver(d.number, p)
            # Add the new driver to the set with the other drivers
            new_drivers = other_drivers | {new_driver} # Add the new driver back in
            # Assume no packages moved with driver and return that state
            # Currently assuming uniform movement cost
            yield (1, State(packages=state.packages, drivers=new_drivers))
            # Now we see if any of the packages could have moved
            for p in state.packages:
                # If they were on the same point as the driver they could have
                # been carried
                if p.point == d.point:
                    # Get a set of all other packages but the current one
                    other_packages = frozenset(state.packages) - {p}
                    # assume the driver carried the package
                    new_package = Package(p.number, new_driver.point)
                    # Add the new package into the set
                    new_packages = other_packages | {new_package}
                    # Currently assuming uniform movement cost
                    yield (1, State(packages=new_packages, drivers=new_drivers))


def h(goal_state, current_state):
    """
    Returns an estimated distance between goal_state and current_state
    """
    total = 0
    # Add up distance of packages from their destinations
    # for (k,v) in goal_state.packages:
    #     p = current_state.packages[k]
    #     total += abs(p.x - v.x) + abs(p.y - v.y)
    return total



def print_path(states):
    for s in states:
        packages = "P: " + " ".join("({}, {}, {})".format(n, p.x, p.y) for (n, p) in s.packages)
        drivers = "D: " + " ".join("({}, {}, {})".format(n, p.x, p.y) for (n, p) in s.drivers)
        print packages, drivers

if __name__ == '__main__':
    problem = pg.get_problem(2, 1, 1, 1)
    nodes = set(problem.grid.nodes())
    t = partial(transition, nodes)
    s = Search(transition_function=t,
           data_structure=Heap(),
           goal_state=problem.goal_state,
           start_state=problem.start_state,
           track_states=True
    )
    cost, states = s()
    print "Goal: ",
    print_path([problem.goal_state])
    print "Start: ",
    print_path([problem.start_state])
    print_path(states)
    print 'Cost:', cost
