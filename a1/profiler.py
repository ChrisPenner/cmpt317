#!/usr/bin/python
from .a1 import transition, cost_of_transition
from .heuristics import h1, h2, h3
from .h4 import h4
from functools import partial
from . import problem_generator as pg
from .a_star.searcher import Searcher
import time
import cProfile, pstats
from .comparison import test_h

if __name__ == "__main__":
    problem = pg.get_problem(size=5, num_drivers=2, num_packages=4, capacity=2, seed=2)

    # This one runs suboptimal on h3:
    # problem = pg.get_problem(size=7, num_drivers=1, num_packages=3, capacity=1, seed=0)

    t = partial(transition, problem)
    s = partial(Searcher,
            transition_function=t,
            cost_function=cost_of_transition,
            start_state=problem.start_state,
            goal_state=problem.goal_state,
            )
    test = partial(test_h, problem, s)

    profile = cProfile.Profile()
    profile.enable()
    test(h4)
    profile.disable()
    ps = pstats.Stats(profile).sort_stats('tottime').print_stats()
