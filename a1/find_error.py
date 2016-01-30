#!/usr/bin/python

from .a1 import run, State
from .problem_generator import get_problem
from .heuristics import h0, h1, h2, h3
from .h4 import h4

size = 2
num_drivers = 1
num_packages = 1

while True:
    for seed in range(5):
        problem = get_problem(size=size, num_drivers=num_drivers, num_packages=num_packages, capacity=1, seed=seed)
        # a_cost, a_steps = run(problem, h2)
        b_cost, b_steps = run(problem, h4)
        print((size, num_drivers, num_packages, seed))
        # if a_cost != b_cost:
            # break
    # if a_cost != b_cost:
        # break
    size += 1
    num_packages += 1

