import problem_generator as pg
from a_star.searcher import Search
from a_star.containers import Heap

def transition(state):
    """
    """
    pass

def h():
    """
    """
    pass

if __name__ == '__main__':
    problem = pg.get_problem(5, 1, 1, 1)
    s = Search(transition_function=transition,
           data_structure=Heap(),
           goal_state=problem.goal_state,
           start_state=problem.start_state,
           track_states=True
    )

    cost, paths = s()
    print cost, paths
