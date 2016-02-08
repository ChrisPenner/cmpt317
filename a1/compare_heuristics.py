#!/usr/bin/python

from __future__ import print_function
import time
from functools import partial
from multiprocessing import Pool

from nkp import run, State
from problem_generator import get_problem, NKP, Point
from heuristics import h0, h1, h2, h3
from h4 import h4

def test_heuristic(problem, heuristic):
    t = time.time()
    cost, steps = run(problem, heuristic)
    # cost, steps = 0, 0
    t_end = time.time() - t
    print(heuristic.__name__, heuristic(problem.goal_state, problem.start_state),cost,steps, '{:.2f}s'.format(t_end), sep=" & ", end=" \\\\\n\\hline\n")

options = {
    'size'  : 10,
    'num_drivers' : 1,
    'num_packages' : 4,
    'capacity' : 2,
    'seed' : 0,
}
problem = get_problem(**options)
print(problem)
print(r'\{ ', r'S={size} \times {size}, D={num_drivers}, K={num_packages}, P={capacity}'.format(**options), r' \}', sep='')

tester = partial(test_heuristic, problem)

# Use all available cores to compute results in parallel
pool = Pool()
pool.map(tester, [
    # h0,
    # h1,
    h2,
    # h3,
    h4,
])
