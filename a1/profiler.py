from a1 import transition, cost_of_transition, hash_state
from heuristics import h1, h2, h3
from functools import partial
import problem_generator as pg
from a_star.searcher import Searcher
from a_star.containers import Heap
import time

problem = pg.get_problem(size=7, num_drivers=1, num_packages=1, capacity=1, seed=3)
hf1 = partial(h1, problem.goal_state)
hf2 = partial(h2, problem.goal_state)
hf3 = partial(h3, problem.goal_state)
t = partial(transition, problem.graph)
s = partial(Searcher,
        transition_function=t,
        cost_function=cost_of_transition,
        start_state=problem.start_state,
        goal_state=problem.goal_state,
        )
s1 = s(data_structure=Heap(heuristic=hf1, hash_state=hash_state))
s2 = s(data_structure=Heap(heuristic=hf2, hash_state=hash_state))
s3 = s(data_structure=Heap(heuristic=hf3, hash_state=hash_state))
t = time.time()
cost1, steps1 = s1()
t1 = time.time() - t
print 'h1', 'Cost:', cost1, 'Steps:', steps1, 'Time:', t1, '100.00%'
t = time.time()
cost2, steps2 = s2()
t2 = time.time() - t
print 'h2', 'Cost:', cost2, 'Steps:', steps2, 'Time:', t2, '{:.2f}%'.format(float(steps2)/steps1 * 100)

t = time.time()
cost3, steps3 = s3()
t3 = time.time() - t
print 'h3', 'Cost:', cost3, 'Steps:', steps3, 'Time:', t3, '{:.2f}%'.format(float(steps3)/steps1 * 100)
