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

