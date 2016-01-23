import problem_generator as pg
from problem_generator import State, Point, Driver
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

def transition(problem, state):
    """
    Returns an iterable of all possible next states and the cost to move there.
    """
    nodes = set(problem.grid.nodes())
    possible_moves = partial(_get_possible_movements, nodes)
    for d in state.drivers:
        # Get a set of all other drivers but the current one
        new_drivers = frozenset(state.drivers) - {d}
        for p in possible_moves(d.point):
            new_driver = Driver(d.number, p)
            new_drivers = new_drivers | {new_driver} # Add the new driver back in
            yield State(packages=state.packages, drivers=new_drivers)
            for p in state.packages:
                if p.point == d.point:
                    new_packages = frozenset(state.packages) - {p}
                    new_package = Package(p.number, new_driver.point)
                    new_packages = new_packages | {new_package}
                    yield State(packages=new_packages, drivers=new_drivers)


def h():
    """
    """
    pass

if __name__ == '__main__':
    problem = pg.get_problem(5, 1, 1, 1)
    t = partial(transition, problem)
    s = Search(transition_function=t,
           data_structure=Heap(),
           goal_state=problem.goal_state,
           start_state=problem.start_state,
           track_states=True
    )

    cost, paths = s()
    print cost, paths
