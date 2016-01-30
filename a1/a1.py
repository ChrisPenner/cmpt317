#!/usr/bin/python
from functools import partial
from itertools import combinations, chain

import problem_generator as pg
from problem_generator import State, Point
from a_star.searcher import Searcher
from a_star.containers import Heap
from heuristics import h1, h2, h3

def transition(problem, state):
    """
    Returns an iterable of all possible next states
    """
    drivers, packages = state.drivers, state.packages
    graph, capacity = problem.graph, problem.capacity
    for (i, driver) in enumerate(drivers):
        # Get drivers that are before and after this one in the tuple, keeping
        # their position in the tuple the same
        before_drivers, after_drivers = drivers[:i], drivers[i+1:]
        for new_driver_position in graph.neighbors(driver):
            new_driver_position = Point(*new_driver_position)
            # Put driver back in appropriate place
            altered_drivers = before_drivers + (new_driver_position,) + after_drivers
            # Now we see if any of the packages could have moved
            # Go through each possible combination we could have with the
            # current capacity, including moving 0 packages
            movable_packages = [ n for (n, package) in enumerate(packages) 
                                if package == driver ]
            # Iterate through the indexes of movable packages for each possible
            # combination
            for c in chain.from_iterable(combinations(movable_packages, r) 
                                         for r in range(0, capacity + 1)):
                # Get new package positions
                new_packages = tuple(new_driver_position if n in c else packages[n] 
                                     for n in range(len(packages)))
                yield State(packages=new_packages, drivers=altered_drivers)

def cost_of_transition(start_state, dest_state):
    # Assume all costs are 1 for now
    return 1

def print_path(states):
    for s in states:
        print("P: ", s.packages, "D: ", s.drivers)

def run(problem, h):
    h = partial(h, problem.goal_state)
    t = partial(transition, problem)
    heap = Heap(heuristic=h)
    s = Searcher(
        transition_function=t,
        cost_function=cost_of_transition,
        data_structure=heap,
        start_state=problem.start_state,
        goal_state=problem.goal_state,
    )
    cost, steps = s()
    return cost, steps


if __name__ == '__main__':
    problem = pg.get_problem(9, 1, 1, 1, seed=0)
    cost, steps = run(problem, h2)
    print("Start: ")
    print_path([problem.start_state])
    print("Goal: ")
    print_path([problem.goal_state])
    print('Cost:')
    print('Steps till optimal:', steps)
