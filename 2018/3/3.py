#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

class MyWork:
    id = ''
    x = 0
    y = 0
    w = 0
    h = 0


class FabricSize:
    x = 0
    y = 0


f = open('puzzle_input.txt', 'r')
fabric = f.readlines()
f.close()

fabric_size = FabricSize()

jobs = []

for part in fabric:
    parts = part.split(' ')
    work = MyWork()
    work.id = parts[0]
    work.x, work.y = (int(x) for x in parts[2].replace(":", "").split(','))
    work.w, work.h = (int(x) for x in parts[3].replace(":", "").rstrip().split('x'))

    # Append the jobs to a list
    jobs.append(work)

    size_x = work.x + work.w
    size_y = work.y + work.h
    if size_x > fabric_size.x:
        fabric_size.x = size_x
    if size_y > fabric_size.y:
        fabric_size.y = size_y

fabric = np.zeros((fabric_size.x + 1, fabric_size.y + 1))

square_overlap_count = 0

for work in jobs:
    for x in range(work.x, work.x + work.w):
        for y in range(work.y, work.y + work.h):
            if fabric[x, y] == 1:
                square_overlap_count += 1
            fabric[x, y] += 1

# Part a
print("Number of overlapping squares: ", square_overlap_count)

# Part b
for work in jobs:
    overlaps = False
    for x in range(work.x, work.x + work.w):
        for y in range(work.y, work.y + work.h):
            if fabric[x, y] > 1:
                overlaps = True
    if not overlaps:
        print("ID: ", work.id, " does not overlap")


