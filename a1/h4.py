from collections import namedtuple
from .heuristics import get_undelivered_packages_and_destinations, packages_to_destinations, manhattan_distance
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
    garage = Point(*goal_state.drivers[0])
    packages, destinations = get_undelivered_packages_and_destinations(current_state.packages, goal_state.packages)
    start_end_pairs = list(zip(packages, destinations))

    # Get all package -> destinations that go a given direction
    # Each package is likely to appear in a north/south list and one east/west
    # list
    with_directions = [(start, end, get_direction(start, end)) for (start, end) in start_end_pairs]
    easts = [ (start.x, end.x) for (start, end, direction) in with_directions if direction[0] == EAST ] 
    wests = [ (start.x, end.x) for (start, end, direction) in with_directions if direction[0] == WEST ] 
    souths = [ (start.y, end.y) for (start, end, direction) in with_directions if direction[1] == SOUTH ] 
    norths = [ (start.y, end.y) for (start, end, direction) in with_directions if direction[1] == NORTH ] 

    # Find the most eastward distance we may have to travel
    east_min = min(easts, key=itemgetter(0))[0] if easts else 0
    east_max = max(easts, key=itemgetter(1))[1] if easts else 0
    west_min = min(wests, key=itemgetter(1))[1] if wests else 0
    west_max = max(wests, key=itemgetter(0))[0] if wests else 0
    south_min = min(souths, key=itemgetter(0))[0] if souths else 0
    south_max = max(souths, key=itemgetter(1))[1] if souths else 0
    north_min = min(norths, key=itemgetter(1))[1] if norths else 0
    north_max = max(norths, key=itemgetter(0))[0] if norths else 0

    # Get actual distance across span
    east_dist = max(east_max - east_min, 0)
    west_dist = max(west_max - west_min, 0)
    north_dist = max(north_max - north_min, 0)
    south_dist = max(south_max - south_min, 0)

    driver_package_distance = 0

    # If there are packages to deliver, find the largest distance from the
    # garage in each cardinal direction
    if packages:
        wester = [ min(start.x, end.x) for start, end in start_end_pairs if min(start.x, end.x) < garage.x ]
        max_west_diff = max(garage.x - x for x in wester) if wester else 0
        easter = [ max(start.x, end.x) for start, end in start_end_pairs if max(start.x, end.x) > garage.x ]
        max_east_diff = max(x - garage.x for x in easter) if easter else 0
        norther = [min(start.y, end.y) for start, end in start_end_pairs if min(start.y, end.y) < garage.y]
        max_north_diff = max(garage.y - y for y in norther) if norther else 0
        souther = [ max(start.y, end.y) for start, end in start_end_pairs if max(start.y, end.y) > garage.y ]
        max_south_diff = max(y - garage.y for y in souther) if souther else 0
        driver_package_distance = max_east_diff + max_west_diff + max_north_diff + max_south_diff

    # Find the distance of drivers from the garage
    driver_distance = sum(manhattan_distance(driver, garage) for driver in current_state.drivers)
    # Use the larger distance (either the packages or the drivers, this helps
    # keep drivers from wandering off)
    driver_distance = max(driver_package_distance, driver_distance)

    # print 'east:', east_dist, 'west:', west_dist, 'north:', north_dist, 'south:', south_dist
    # print [get_direction(start, end) for start, end in start_end_pairs]
    # print "undelivered:", packages
    # print "pairs:", start_end_pairs
    # print "Easts:", easts, 'Wests:', wests
    # print "Norths:", norths, 'Souths:', souths
    # print "start:", current_state
    # print "end:", goal_state

    total_package_distance =  east_dist + west_dist + north_dist + south_dist
    return total_package_distance + driver_distance
