#!/usr/bin/python

import time

from nkp import run, State
from problem_generator import get_problem, NKP, Point
from heuristics import h0, h1, h2, h3
from h4 import h4

def test_heuristic(problem, heuristic):
    t = time.time()
    cost, steps = run(problem, heuristic)
    t_end = time.time() - t
    print(heuristic.__name__, "Heuristic Guess:", heuristic(problem.goal_state, problem.start_state), 'Cost:', cost, 'Steps:', steps, 'Time: {:.2f}s'.format(t_end))

problem = get_problem(size=1, num_drivers=1, num_packages=1, capacity=10, seed=0)
print problem

test_heuristic(problem, h2)
