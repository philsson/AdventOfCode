#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

import matplotlib.pyplot as plt

ll = None
ur = None


class Zone:

    def __init__(self, x=0, y=0):
        self.extreme = False
        self.x = x
        self.y = y
        self.proximities = 0  # For use in assignment B


def read_zones():
    f = open('puzzle_input.txt', 'r')
    #f = open('test_input.txt', 'r')
    #f = open('my_test_input.txt', 'r')
    zone_strings = f.readlines()
    f.close()

    id = 0
    zones = {}
    for zone_string in zone_strings:
        zone = Zone()
        zone.x, zone.y = (int(x) for x in zone_string.rstrip().split(','))
        zones[id] = zone
        id += 1

    return zones


def find_corners(zones):

    for id, zone in zones.items():
        global ll, ur

        x = zone.x
        y = zone.y

        if ll is None or ur is None:
            ll = [x, y]
            ur = [x, y]

        if x < ll[0]:  # x min
            ll[0] = x
        if y < ll[1]:  # y min
            ll[1] = y
        if x > ur[0]:
            ur[0] = x  # x max
        if y > ur[1]:
            ur[1] = y  # y max


def find_extremes(m: np.matrix, zones):

    width, height = m.shape

    extreme_map = {}

    for x in range(0, width - 1):
        extreme_map[m[x, 0]] = True
        extreme_map[m[x, height - 1]] = True
    for y in range(0, height - 1):
        extreme_map[m[0, y]] = True
        extreme_map[m[width - 1, y]] = True

    for id, value in extreme_map.items():
        if id != -1:
            zones[id].extreme = True


def print_zones(zones):
    for id, zone in zones.items():
        print("ID:", id, " @ ", zone.x, ",", zone.y, sep='')


def distance(a: Zone, b: Zone):
    return abs(a.x - b.x) + abs(a.y - b.y)

def calc_dist_matrix(zones):
    width = ur[0] - ll[0] + 1
    height = ur[1] - ll[1] + 1
    offset_x = ll[0]
    offset_y = ll[1]

    m = np.full((width, height), np.inf)

    for x in range(0, width):
        for y in range(0, height):
            winning_id = None
            dist_equal = False

            min_dist_hit = 0
            for id, zone in zones.items():
                dist = distance(zone, Zone(x + offset_x, y + offset_y))

                #print("dist:", dist)
                if dist < m[x, y]:
                    m[x, y] = dist
                    winning_id = id
                    min_dist_hit = 1
                    dist_equal = False
                elif dist == m[x, y]:
                    min_dist_hit += 1
                if min_dist_hit >= 2:
                    dist_equal = True
            m[x, y] = winning_id
            if dist_equal:
                m[x, y] = -1

    #print(m.transpose())
    print("Matrix created of size", m.shape)
    return m


def find_biggest_area(m: np.matrix, zones):

    sizes = {}

    for x in range(0, m.shape[0]):
        for y in range(0, m.shape[1]):
            if m[x, y] in sizes:
                sizes[m[x, y]] += 1
            else:
                sizes[m[x, y]] = 1

    max_size = 0
    winning_zone = -1
    for id, size in sizes.items():
        if id in zones and size > max_size and not zones[id].extreme:
            max_size = size
            winning_zone = id

    return max_size, winning_zone

def plot_zones(m: np.matrix, zones):
    width = ur[0] - ll[0] + 1
    height = ur[1] - ll[1] + 1
    offset_x = ll[0]
    offset_y = ll[1]

    plt.matshow(m.transpose())
    for id, zone in zones.items():
        plt.plot(zone.x - offset_x + 0*width, zone.y - offset_y + 0*height, '.-')
    plt.show()


def find_proximities(zones):

    threshold = 10000
    #threshold = 32

    region_size = 0
    for x in range(ll[0], ur[0]):
        for y in range(ll[1], ur[1]):
            total_dist = 0
            for id, zone in zones.items():
                total_dist += distance(zone, Zone(x, y))
            if total_dist < threshold:
                region_size += 1
    return region_size


# Parse zones from file
zones = read_zones()

# print the parsed zones
#print_zones(zones)

# Find the corners
find_corners(zones)

# Create the matrix
m = calc_dist_matrix(zones)

# Find extremes (infinite areas)
find_extremes(m, zones)

# Find largest finite area
max_area, winning_id = find_biggest_area(m, zones)
if winning_id != -1:
    print("A:", "Largest area of", max_area, "by id", winning_id,
          "@", zones[winning_id].x, ",", zones[winning_id].y,
          "(", zones[winning_id].x - ll[0], ",", zones[winning_id].y - ll[1], ")")
else:
    print("All zones where extremes")

# Assignment B
region_size = find_proximities(zones)
print("B: The region size is", region_size)

# Plot the result
plot_zones(m, zones)



