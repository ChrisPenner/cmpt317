#!/usr/bin/python
from .a1 import transition, cost_of_transition
from .heuristics import h1, h2, h3
from .h4 import h4
from functools import partial
from . import problem_generator as pg
from .a_star.searcher import Searcher
from .a_star.containers import Heap
import time
from multiprocessing import Pool

def test_h(problem, s, h):
    hf = partial(h, problem.goal_state)
    sf = s(data_structure=Heap(heuristic=hf))
    t = time.time()
    cost, steps = sf()
    t_end = time.time() - t
    if steps == 0:
        efficiency = 100
    else:
        efficiency = float(cost)/steps * 100

    print((h.__name__, 'Cost:', cost, 'Steps:', steps, 'Time: {:.2f}s'.format(t_end), 'Efficiency: {:.2f}%'.format(efficiency)))

if __name__ == '__main__':
    problem = pg.get_problem(size=6, num_drivers=1, num_packages=3, capacity=1, seed=1)

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

    # Use all available cores to compute results
    pool = Pool()
    pool.map(test, [
        # h1,
        h2,
        # h3,
        h4,
    ])
