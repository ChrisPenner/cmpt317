#!/usr/bin/python

from nkp import run, State
from problem_generator import get_problem
from heuristics import h0, h1, h2, h3
from h4 import h4

size = 3
num_drivers = 1
num_packages = 1
heuristic = h2

# Run consistently larger and larger problems.
while True:
    for seed in range(5):
        problem = get_problem(size=size, num_drivers=num_drivers, num_packages=num_packages, capacity=20, seed=seed)
        guess = heuristic(problem.goal_state, problem.start_state)
        cost, steps = run(problem, heuristic)
        print size, num_drivers, num_packages, seed
        print "Guess/cost:", guess, cost
    size += 1
    num_packages += 1

