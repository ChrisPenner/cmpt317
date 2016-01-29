#!/usr/bin/python
from functools import partial

import problem_generator as pg
from problem_generator import State, Point
from a_star.searcher import Searcher
from a_star.containers import Heap
from heuristics import h1, h2, h3

def transition(problem, state):
    """
    Returns an iterable of all possible next states
    """
    graph, capacity = problem.graph, problem.capacity
    for (d_num, d_point) in state.drivers.iteritems():
        for new_driver_position in graph.neighbors(d_point):
            altered_drivers = state.drivers.copy()
            altered_drivers[d_num] = new_driver_position

            # Assume no packages moved with driver and return that state
            yield State(packages=state.packages, drivers=altered_drivers)
            # Now we see if any of the packages could have moved
            for (p_num, p_point) in state.packages.iteritems():
                # If they were on the same point as the driver they could have
                # been carried
                if p_point == d_point:
                    altered_packages = state.packages.copy()
                    # assume the driver carried the package
                    altered_packages[p_num]= new_driver_position
                    yield State(packages=altered_packages, drivers=altered_drivers)

def cost_of_transition(start_state, dest_state):
    # Assume all costs are 1 for now
    return 1

def hash_state(state):
    """
    Turns the state object (which uses dicts) into a tuple of frozensets 
    (which can be hashed) so we can store it and check for repetition in O(1)
    within the heap.
    """
    freeze = lambda x: frozenset(x.iteritems())
    return tuple(freeze(x) for x in state)

def print_path(states):
    for s in states:
        print "P: ", s.packages, "D: ", s.drivers

def run(problem, h):
    h = partial(h, problem.goal_state)
    t = partial(transition, problem)
    heap = Heap(heuristic=h, hash_state=hash_state)
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
    print "Start: ",
    print_path([problem.start_state])
    print "Goal: ",
    print_path([problem.goal_state])
    print 'Cost:', cost
    print 'Steps till optimal:', steps
