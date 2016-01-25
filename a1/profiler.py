from a1 import transition, cost_of_transition, hash_state
from heuristics import h1, h2, h3
from functools import partial
import problem_generator as pg
from a_star.searcher import Searcher
from a_star.containers import Heap
import time

def test_h(problem, h, s):
    hf = partial(h, problem.goal_state)
    sf = s(data_structure=Heap(heuristic=hf, hash_state=hash_state))
    t = time.time()
    cost, steps = sf()
    t_end = time.time() - t
    print 'Cost:', cost, 'Steps:', steps, 'Time: {:.2f}s'.format(t_end), 'Efficiency: {:.2f}%'.format(float(cost)/steps * 100)

# problem = pg.get_problem(size=7, num_drivers=1, num_packages=3, capacity=1, seed=1)

# This one runs suboptimal on h3:
# problem = pg.get_problem(size=7, num_drivers=1, num_packages=3, capacity=1, seed=0)

t = partial(transition, problem.graph)
s = partial(Searcher,
        transition_function=t,
        cost_function=cost_of_transition,
        start_state=problem.start_state,
        goal_state=problem.goal_state,
        )

print 'h1',
test_h(problem, h1, s)
print 'h2',
test_h(problem, h2, s)
print 'h3',
test_h(problem, h3, s)
