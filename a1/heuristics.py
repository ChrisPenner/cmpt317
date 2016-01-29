from operator import itemgetter
from itertools import combinations, product

def manhattan_distance((ax, ay), (bx, by)):
    return abs(ax - bx) + abs(ay - by)

def packages_to_destinations(packages, destinations):
    return (manhattan_distance(p, d) for p, d in zip(packages, destinations))

def get_undelivered_packages_and_destinations(packages, destinations):
    p = tuple(package for package, destination in zip(packages, destinations)
                     if package != destination)
    d = tuple(package for package, destination in zip(packages, destinations)
                     if package != destination)
    return p, d

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
    for (package, destination) in zip(current_state.packages, goal_state.packages):
        px, py = package
        dx, dy = destination
        total += abs(px - dx) + abs(py - dy)
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
    garage = goal_state.drivers[0]

    # Add up distance of packages from their destinations
    for (package, destination) in zip(current_state.packages, goal_state.packages):
        distance_from_dest = manhattan_distance(package, destination)
        total_package_distance += distance_from_dest
        if distance_from_dest != 0:
            undelivered_packages += 1
            driver_distance_from_undelivered_packages += manhattan_distance(driver, package)

    if undelivered_packages == 0:
        driver_distance_from_garage = sum(manhattan_distance(d, garage)
                                          for d in current_state.drivers)

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
    packages, destinations = get_undelivered_packages_and_destinations(current_state.packages, goal_state.packages)

    if packages:
        package_distances = packages_to_destinations(packages, destinations)
        largest_package_distance_from_dest = max(package_distances)

        # Get the distance from the furthest (from its destination) package from
        # the undelivered package that is furthest from it, could be zero
        if len(packages) > 1:
            furthest_package_from_furthest_package = max(manhattan_distance(a,b)
                                                        for (a,b) in combinations(packages, r=2))

        # Use the shortest distance of any driver to any package, it's all that we
        # can guarantee
        min_driver_to_package_distance = min(manhattan_distance(a, b) for (a, b) in product(current_state.drivers, packages))
    else:
        # No undelivered_packages, we need to get all drivers back to the garage
        driver_distance_from_garage = sum(manhattan_distance(d, garage)
                                          for d in current_state.drivers)

    return (
         largest_package_distance_from_dest
        + min_driver_to_package_distance
        + driver_distance_from_garage
    )
