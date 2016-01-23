import problem_generator as pg
from problem_generator import State, Point
from a_star.searcher import Search
from a_star.containers import Heap
from functools import partial

def _get_possible_movements(nodes, point):
    """
    Return all possible nodes that can be reached in the graph given point p
    """
    x,y = point
    return [p for p in [Point(x - 1, y), Point(x + 1, y),
                        Point(x, y - 1), Point(x, y + 1)]
            if p in nodes]

def transition(nodes, state):
    """
    Returns an iterable of all possible next states and the cost to move there
    of the form (cost, next_state)
"""
    possible_moves = partial(_get_possible_movements, nodes)
    for (d_num, d_point) in state.drivers.iteritems():
        for new_driver_position in possible_moves(d_point):
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



def print_path(states):
    for s in states:
        print "P: ", s.packages, "D: ", s.drivers

if __name__ == '__main__':
    problem = pg.get_problem(2, 1, 1, 1)
    goal_state = problem.goal_state
    h = partial(h1, goal_state)
    nodes = set(problem.grid.nodes())
    t = partial(transition, nodes)
    s = Search(transition_function=t,
               cost_function=cost_of_transition,
               data_structure=Heap(heuristic=h),
               goal_state=problem.goal_state,
               start_state=problem.start_state,
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
