from operator import itemgetter
from itertools import combinations, product

def manhattan_distance((ax, ay), (bx, by)):
    return abs(ax - bx) + abs(ay - by)

def packages_to_destinations(destinations, packages):
    total = 0
    return {package_num: manhattan_distance(loc, destinations[package_num])
            for (package_num, loc) in packages.iteritems() }

def get_undelivered_packages(packages, destinations):
    return {k:v for k,v in packages.iteritems() if v != destinations[k]}

def h0(goal, current):
    return 0

# NOT ADMISSIBLE!!
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

# NOT ADMISSIBLE!!
def h2(goal_state, current_state):
    """
    Returns an estimated distance between goal_state and current_state

    h2 tries to move drivers towards packages, then packages towards destinations,
    then drivers back to garages
    """
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

# Admissible :)
def h3(goal_state, current_state):
    """
    Returns an estimated distance between goal_state and current_state

    h3 tries to move drivers towards packages, then packages towards destinations,
    then drivers back to garages
    """
    driver_distance_from_garage = 0
    garage = goal_state.drivers[0]
    min_driver_to_package_distance = 0
    largest_package_distance_from_dest = 0
    furthest_package_from_furthest_package = 0

    # Get all undelivered packages
    undelivered_packages = get_undelivered_packages(current_state.packages, goal_state.packages)

    if undelivered_packages:
        package_distances = packages_to_destinations(goal_state.packages, undelivered_packages)
        furthest_package_num, largest_package_distance_from_dest = max(package_distances.iteritems(), key=itemgetter(1))

        # Get the distance from the furthest (from its destination) package from
        # the undelivered package that is furthest from it, could be zero
        if len(undelivered_packages) > 1:
            furthest_package_from_furthest_package = max(manhattan_distance(a,b)
                                                        for (a,b) in combinations(undelivered_packages.itervalues(), r=2))

        # Use the shortest distance of any driver to any package, it's all that we
        # can guarantee
        min_driver_to_package_distance = min(manhattan_distance(a, b) for (a, b) in product(current_state.drivers.itervalues(), undelivered_packages.itervalues()))
    else:
        # No undelivered_packages, we need to get all drivers back to the garage
        driver_distance_from_garage = sum(manhattan_distance(d, garage)
                                          for d in current_state.drivers.itervalues())

    return (
         largest_package_distance_from_dest
        + min_driver_to_package_distance
        + driver_distance_from_garage
    )
