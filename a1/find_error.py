#!/usr/bin/python

from a1 import run, State
from problem_generator import get_problem
from heuristics import h0, h1, h2, h3
from h4 import h4

size = 3
num_drivers = 1
num_packages = 1

while True:
    for seed in range(5):

        problem = get_problem(size=size, num_drivers=num_drivers, num_packages=num_packages, capacity=20, seed=seed)
        # a_cost, a_steps = run(problem, h2)
        guess = h2(problem.goal_state, problem.start_state)
        b_cost, b_steps = run(problem, h2)
        print(size, num_drivers, num_packages, seed)
        print "Guess/cost:", guess, b_cost
        # if a_cost < b_cost:
        #     raise Exception()
        # if b_cost - guess >= 10:
        #     raise Exception()
        # if guess > b_cost:
        #     break
    # if guess > b_cost:
        # break
        # if a_cost != b_cost:
            # break
    # if a_cost != b_cost:
        # break
    size += 1
    num_packages += 1

