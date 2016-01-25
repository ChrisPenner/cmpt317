from a1 import run
from problem_generator import get_problem
from heuristics import h1, h2, h3

def test_heuristic(problem, heuristic):
    cost, steps = run(problem, heuristic)
    print heuristic.__name__, "Guess:", heuristic(problem.goal_state, problem.start_state), 'Cost:', cost, 'Steps:', steps

problem = get_problem(size=4, num_drivers=1, num_packages=3, capacity=1, seed=None)
test_heuristic(problem, h1)
test_heuristic(problem, h2)
test_heuristic(problem, h3)
