import problem_generator as pg
from problem_generator import State, Point
from a_star.searcher import Searcher
from a_star.containers import Heap
from functools import partial

def transition(graph, state):
    """
    Returns an iterable of all possible next states and the cost to move there
    of the form (cost, next_state)
    """
    for (d_num, d_point) in state.drivers.iteritems():
        for new_driver_position in graph.neighbors(d_point):
            # Get a all other drivers but the current one
            altered_drivers = state.drivers.copy()
            altered_drivers[d_num] = new_driver_position

            # Assume no packages moved with driver and return that state
            yield State(packages=state.packages, drivers=altered_drivers)
            # Now we see if any of the packages could have moved
            for (p_num, p_point) in state.packages.iteritems():
                # If they were on the same point as the driver they could have
                # been carried
                if p_point == d_point:
                    altered_packages = state.packages.copy()
                    # assume the driver carried the package
                    altered_packages[p_num]= new_driver_position
                    yield State(packages=altered_packages, drivers=altered_drivers)

def cost_of_transition(start_state, dest_state):
    # Assume all are cost 1
    return 1

def h1(goal_state, current_state):
    """
    Returns an estimated distance between goal_state and current_state
    """
    total = 0
    # Add up distance of packages from their destinations
    for (k,v) in goal_state.packages.iteritems():
        px, py = current_state.packages[k]
        vx, vy = v
        total += abs(px - vx) + abs(py - vy)
    return total

def hash_state(state):
    freeze = lambda x: frozenset(x.iteritems())
    return tuple(map(freeze, state))

def print_path(states):
    for s in states:
        print "P: ", s.packages, "D: ", s.drivers

if __name__ == '__main__':
    problem = pg.get_problem(2, 1, 1, 1)
    goal_state = problem.goal_state
    h = partial(h1, goal_state)
    t = partial(transition, problem.graph)
    s = Searcher(transition_function=t,
               cost_function=cost_of_transition,
               data_structure=Heap(heuristic=h, hash_state=hash_state),
               start_state=problem.start_state,
               goal_state=problem.goal_state,
               track_states=True
    )
    cost, states = s()
    print "Start: ",
    print_path([problem.start_state])
    print "Goal: ",
    print_path([problem.goal_state])
    print "Path: "
    print_path(states)
    print 'Cost:', cost
