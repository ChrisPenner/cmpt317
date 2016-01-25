def manhattan_distance((ax, ay), (bx, by)):
    return abs(ax - bx) + abs(ay - by)

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

def h3(goal_state, current_state):
    """
    Returns an estimated distance between goal_state and current_state

    h3 tries to move drivers towards packages, then packages towards destinations,
    then drivers back to garages
    """
    total_package_distance = 0
    driver_distance_from_undelivered_packages = 0
    undelivered_packages = 0
    driver_distance_from_garage = 0
    undelivered_return_path = 0
    garage = goal_state.drivers[0]

    # Add up distance of packages from their destinations
    for (package_num, destination) in goal_state.packages.iteritems():
        package_loc = current_state.packages[package_num]
        distance_from_dest = manhattan_distance(package_loc, destination)
        total_package_distance += distance_from_dest
        if distance_from_dest != 0:
            undelivered_packages += 1
            # Use the distance of the closest driver to guarantee admissibility
            driver_distance_from_undelivered_packages += min(
                manhattan_distance(d, package_loc)
                for d in current_state.drivers.itervalues())

            # If it's undelivered, we know we can add at least the distance 
            # between its destination and the garage
            undelivered_return_path += manhattan_distance(destination, garage)

    if undelivered_packages == 0:
        driver_distance_from_garage = sum(manhattan_distance(d, garage)
                                          for d in current_state.drivers.itervalues())

    return (total_package_distance
            + driver_distance_from_undelivered_packages
            + driver_distance_from_garage
            + undelivered_return_path
            )
