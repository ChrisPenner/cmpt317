from collections import namedtuple
from heuristics import get_undelivered_packages_and_destinations, packages_to_destinations, manhattan_distance
from operator import itemgetter
Point = namedtuple('Point', ['x', 'y'])
EAST = 'east'
WEST = 'west'
NORTH = 'north'
SOUTH = 'south'
NONE = 'none'

def get_direction(start, end):
    if start.x < end.x:
        horizontal = EAST
    elif start.x > end.x:
        horizontal = WEST
    else:
        horizontal = NONE

    if start.y < end.y:
        vertical = SOUTH
    elif start.y > end.y:
        vertical = NORTH
    else:
        vertical = NONE
    return (horizontal, vertical)

# Should be admissible
def h4(goal_state, current_state):
    garage = goal_state.drivers[0]
    packages, destinations = get_undelivered_packages_and_destinations(current_state.packages, goal_state.packages)

    # Find the distance of drivers from the garage
    driver_distance = sum(manhattan_distance(driver, garage) for driver in current_state.drivers)

    if not packages:
        return driver_distance

    start_end_pairs = zip(packages, destinations)

    # Get all package -> destinations that go a given direction
    # Each package is likely to appear in a north/south list and one east/west
    # list
    with_directions = [(start, end, get_direction(start, end)) for (start, end) in start_end_pairs]
    easts = [ (start.x, end.x) for (start, end, direction) in with_directions if direction[0] == EAST ] 
    wests = [ (start.x, end.x) for (start, end, direction) in with_directions if direction[0] == WEST ] 
    souths = [ (start.y, end.y) for (start, end, direction) in with_directions if direction[1] == SOUTH ] 
    norths = [ (start.y, end.y) for (start, end, direction) in with_directions if direction[1] == NORTH ] 

    total_package_distance = 0
    # Find the most eastward distance we may have to travel
    if easts:
        east_min = min(easts, key=itemgetter(0))[0]
        east_max = max(easts, key=itemgetter(1))[1]
        east_dist = east_max - east_min
        total_package_distance += east_dist
    if wests:
        west_min = min(wests, key=itemgetter(1))[1]
        west_max = max(wests, key=itemgetter(0))[0]
        west_dist = west_max - west_min
        total_package_distance += west_dist
    if souths:
        south_min = min(souths, key=itemgetter(0))[0]
        south_max = max(souths, key=itemgetter(1))[1]
        south_dist = south_max - south_min
        total_package_distance += south_dist
    if norths:
        north_min = min(norths, key=itemgetter(1))[1]
        north_max = max(norths, key=itemgetter(0))[0]
        north_dist = north_max - north_min
        total_package_distance += north_dist

    # Get the offset required to move from one directional run to another.
    if norths and souths:
        northern_offset = abs(north_min - south_min)
        southern_offset = abs(north_max - south_max)
        if garage.y > min(north_max, south_max):
            north_south_offset = northern_offset
        elif garage.y < max(north_min, south_min):
            north_south_offset = southern_offset
        else:
            north_south_offset = northern_offset + southern_offset
    else:
        north_south_offset = 0
    if easts and wests:
        western_offset = abs(east_min - west_min)
        eastern_offset = abs(east_max - west_max)
        if garage.x > min(east_max, west_max):
            east_west_offset = western_offset
        elif garage.x < max(east_min, west_min):
            east_west_offset = eastern_offset
        else:
            east_west_offset = abs(west_min - east_min) + abs(east_max - west_max)
    else:
        east_west_offset = 0
    total_offset = north_south_offset + east_west_offset


    # Get minimum distance of any driver to the closest (undelivered) package
    if packages:
        starting_travel = min(manhattan_distance(driver, package)
                            for driver in current_state.drivers
                            for package in packages)
        ending_travel = min(manhattan_distance(destination, garage)
                            for destination in destinations)
    else:
        starting_travel = ending_travel = 0

    # print 'ewns', east_dist, west_dist, north_dist#, south_dist
    # print 'Travels:', starting_travel, ending_travel
    # print 'eastwest offset / northsouth offset', east_west_offset, north_south_offset
    # print 'driver distance or total_offset', driver_distance, total_offset
    # print 'total package distance', total_package_distance
    return total_package_distance + total_offset + starting_travel + ending_travel
