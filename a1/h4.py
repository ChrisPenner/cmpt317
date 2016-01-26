from collections import namedtuple
from heuristics import get_undelivered_packages, packages_to_destinations, manhattan_distance
from operator import itemgetter
Point = namedtuple('Point', ['x', 'y'])
EAST = 'east'
WEST = 'west'
NORTH = 'north'
SOUTH = 'south'
NONE = 'none'

def get_direction(start, end):
    start, end = Point(*start), Point(*end)
    if start.x < end.x:
        horizontal = EAST
    elif start.x == end.x:
        horizontal = NONE
    else:
        horizontal = WEST

    if start.y < end.y:
        vertical = SOUTH
    elif start.y == end.y:
        vertical = NONE
    else:
        vertical = NORTH
    return (horizontal, vertical)


class Area(object):
    EAST = 'east'
    WEST = 'west'
    NORTH = 'north'
    SOUTH = 'south'
    NONE = 'none'

    def __init__(self, start, end):
        self.start = Point(*start)
        self.end = Point(*end)
        self.width = abs(self.start.x - self.end.x)
        self.height = abs(self.start.y - self.end.y)

        self.left = min(self.start.x, self.end.x)
        self.right = max(self.start.x, self.end.x)
        self.top = min(self.start.y, self.end.y)
        self.bottom = max(self.start.y, self.end.y)

        if self.start.x < self.end.x:
            self.horizontal = Area.EAST
        elif self.start.x == self.end.x:
            self.horizontal = Area.NONE
        else:
            self.horizontal = Area.WEST

        if self.start.y < self.end.y:
            self.vertical = Area.SOUTH
        elif self.start.y == self.end.y:
            self.vertical = Area.NONE
        else:
            self.vertical = Area.NORTH

    def __eq__(self, other):
        return (self.start == other.start and self.end == other.end)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '(Start: {}, End: {})'.format(self.start, self.end)

    def contains(self, area):
        """ Does self contain area? """
        return (self.left < area.left and self.right > area.right
                and self.top < area.top and self.bottom > area.bottom)

    def coalesce(self, area):
        """
        Tries to combine compatible areas in any way possible
        returns a list of the new Areas that must be traversed
        """
        if self.horizontal != area.horizontal and self.vertical != area.vertical:
            # We know that we don't share any directionality, might as well
            # just leave them as is, even if we intersect
            return [self, area]

        new_left = max(self.left, area.left)
        new_right = min(self.right, area.right)

        new_top = max(self.top, area.top)
        new_bottom = min(self.bottom, area.bottom)
        if new_top > new_bottom or new_left > new_right:
            # No intersection
            return [self, area]

        intersection = Area((new_left, new_top), (new_right, new_bottom))
        return [intersection]

# Should be admissible
def h4(goal_state, current_state):
    destinations = goal_state.packages
    garage = Point(*goal_state.drivers[0])
    undelivered_packages = get_undelivered_packages(current_state.packages, goal_state.packages)
    start_end_pairs = [(Point(*start), Point(*destinations[num])) for num, start in undelivered_packages.iteritems()]

    # start_end_pairs.extend((Point(*driver), Point(*goal_state.drivers[num])) for num, driver in current_state.drivers.iteritems())

    easts = [ (start.x, end.x) for (start, end) in start_end_pairs if get_direction(start, end)[0] == EAST ] 
    wests = [ (start.x, end.x) for (start, end) in start_end_pairs if get_direction(start, end)[0] == WEST ] 
    souths = [ (start.y, end.y) for (start, end) in start_end_pairs if get_direction(start, end)[1] == SOUTH ] 
    norths = [ (start.y, end.y) for (start, end) in start_end_pairs if get_direction(start, end)[1] == NORTH ] 

    # print [get_direction(start, end) for start, end in start_end_pairs]

    # print "undelivered:", undelivered_packages
    # print "pairs:", start_end_pairs
    # print "Easts:", easts, 'Wests:', wests
    # print "Norths:", norths, 'Souths:', souths
    # print "start:", current_state
    # print "end:", goal_state

    east_min = min(easts, key=itemgetter(0))[0] if easts else 0
    east_max = max(easts, key=itemgetter(1))[1] if easts else 0
    west_min = min(wests, key=itemgetter(1))[1] if wests else 0
    west_max = max(wests, key=itemgetter(0))[0] if wests else 0
    north_min = min(norths, key=itemgetter(0))[0] if norths else 0
    north_max = max(norths, key=itemgetter(1))[1] if norths else 0
    south_min = min(souths, key=itemgetter(1))[1] if souths else 0
    south_max = max(souths, key=itemgetter(0))[0] if souths else 0

    east_dist = max(east_max - east_min, 0)
    west_dist = max(west_min - west_max, 0)
    north_dist = max(north_min - north_max, 0)
    south_dist = max(south_max - south_min, 0)

    if undelivered_packages:
        max_hor = max(abs(garage.x - start.x) for start, end in start_end_pairs)
        max_vert = max(abs(garage.y - start.y) for start, end in start_end_pairs)
        driver_distance = max_hor + max_vert
    else:
        driver_distance = sum(manhattan_distance(driver, garage) for driver in current_state.drivers.itervalues())

    # print 'east:', east_dist, 'west:', west_dist, 'north:', north_dist, 'south:', south_dist

    total_package_distance =  east_dist + west_dist + north_dist + south_dist
    return total_package_distance + driver_distance
