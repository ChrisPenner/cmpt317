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
    # Assume all costs are 1 for now
    return 1

def h1(goal_state, current_state):
    """
    Returns an estimated distance between goal_state and current_state

    h1 only counts the distance of packages from their goal.
    """
    total = 0
    # Add up distance of packages from their destinations
    for (k,v) in goal_state.packages.iteritems():
        px, py = current_state.packages[k]
        vx, vy = v
        total += abs(px - vx) + abs(py - vy)
    return total

def h2(goal_state, current_state):
    """
    Returns an estimated distance between goal_state and current_state

    h2 tries to move drivers towards packages, then packages towards destinations,
    then drivers back to garages
    """
    manhattan_distance = lambda (ax, ay), (bx, by): abs(ax - bx) + abs(ay - by)
    total_package_distance = 0
    driver_distance_from_undelivered_packages = 0
    driver = current_state.drivers[0]
    undelivered_packages = 0
    driver_distance_from_garage = 0

    # Add up distance of packages from their destinations
    for (k,v) in goal_state.packages.iteritems():
        package_loc = current_state.packages[k]
        distance_from_dest = manhattan_distance(package_loc, v)
        total_package_distance += distance_from_dest
        if distance_from_dest != 0:
            undelivered_packages += 1
            driver_distance_from_undelivered_packages += manhattan_distance(driver, package_loc)

    if undelivered_packages == 0:
        driver_distance_from_garage = sum(manhattan_distance(d, goal_state.drivers[0])
                                          for d in current_state.drivers.itervalues())

    return (total_package_distance
            + driver_distance_from_undelivered_packages
            + driver_distance_from_garage
            )

def hash_state(state):
    """
    Turns the state object (which uses dicts) into a tuple of frozensets 
    (which can be hashed) so we can store it and check for repetition in O(1)
    within the heap.
    """
    freeze = lambda x: frozenset(x.iteritems())
    return tuple(freeze(x) for x in state)

def print_path(states):
    for s in states:
        print "P: ", s.packages, "D: ", s.drivers

if __name__ == '__main__':
    problem = pg.get_problem(33, 1, 1, 1, seed=0)
    h = partial(h1, problem.goal_state)
    t = partial(transition, problem.graph)
    heap = Heap(heuristic=h, hash_state=hash_state)
    s = Searcher(
        transition_function=t,
        cost_function=cost_of_transition,
        data_structure=heap,
        start_state=problem.start_state,
        goal_state=problem.goal_state,
    )
    cost, steps = s()
    print "Start: ",
    print_path([problem.start_state])
    print "Goal: ",
    print_path([problem.goal_state])
    print 'Cost:', cost
    print 'Steps till optimal:', steps
