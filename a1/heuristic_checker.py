#!/usr/bin/python

from a1 import run, State
from problem_generator import get_problem
from heuristics import h0, h1, h2, h3
from h4 import h4

def test_heuristic(problem, heuristic):
    cost, steps = run(problem, heuristic)
    # print "Guess:", heuristic(problem.goal_state, problem.start_state)
    print heuristic.__name__, "Guess:", heuristic(problem.goal_state, problem.start_state), 'Cost:', cost, 'Steps:', steps

problem = get_problem(size=4, num_drivers=1, num_packages=3, capacity=1, seed=0)
# test_heuristic(problem, h0)
# test_heuristic(problem, h1)
# test_heuristic(problem, h2)
# test_heuristic(problem, h3)
test_heuristic(problem, h4)
# print problem.goal_state


# Notes:
# h2 is suboptimal on: get_problem(size=4, num_drivers=1, num_packages=3, capacity=1, seed=0)
