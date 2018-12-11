#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from copy import deepcopy
import numpy as np
import matplotlib.pyplot as plt
from parse import *

#filename = 'test_input.txt'
filename = 'puzzle_input.txt'
wait = 100  # Time to wait after plotting the result


def parse_star(line):
    p = parse('position=<{:d},{:d}>velocity=<{:d},{:d}>', line.replace(' ',''))
    return np.matrix([p[0], p[1]]), np.matrix([p[2], p[3]], dtype=np.int)


def parse_stars(filename):

    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    nr_of_points = len(lines)

    star_positions = np.zeros((nr_of_points, 2), dtype=int)
    star_velocities = np.zeros((nr_of_points, 2), dtype=int)

    index = 0
    for line in lines:
        pos, vel = parse_star(line)
        star_positions[index, :] = pos[0, :]
        star_velocities[index, :] = vel[0, :]
        index += 1

    return star_positions, star_velocities


class Sky:

    def __init__(self, m, m_v):
        self.x_min = m[:, 0].min()
        self.x_max = m[:, 0].max()
        self.y_min = m[:, 1].min()
        self.y_max = m[:, 1].max()
        self.initial_pos = deepcopy(m)
        self.last_pos = m  # TODO: deepcopy?
        self.velocities = m_v
        self.m = np.zeros((self.x_max - self.x_min + 1, self.y_max - self.y_min + 1), dtype=bool)
        self.input_size = m.shape[0]
        self.fill(m)
        initial_width = self.x_max - self.x_min
        self.marker_size = 600/initial_width

    def fill(self, m, state = True):
        for x in range(0, self.input_size):
            try:
                self.m[m[x, 0] - self.x_min, m[x, 1] - self.y_min] = state
            except:
                return False
        return True

    def step(self, steps):
        self.fill(self.last_pos, False)
        self.last_pos += steps*self.velocities
        return self.fill(self.last_pos, True)

    def plot(self):

        x_min = self.last_pos[:, 0].min()
        x_max = self.last_pos[:, 0].max()
        y_min = self.last_pos[:, 1].min()
        y_max = self.last_pos[:, 1].max()

        # TODO: Why the plus 1?
        plt.matshow(self.m[x_min - self.x_min:x_max - self.x_min + 1,
                    y_min - self.y_min:y_max - self.y_min + 1].transpose())

        plt.axis('off')
        plt.pause(wait)

    def get_width(self):
        return self.last_pos[:, 0].max() - self.last_pos[:, 0].min()


# The program
stars, velocities = parse_stars(filename)
sky = Sky(stars, velocities)

plt.ion()
fig = plt.figure()

last_width = sky.get_width()
step = 0
for x in range(0, 10000000):

    print("Time:", step)

    if sky.step(1) is not True:
        print("END")
        break

    width = sky.get_width()
    if width > last_width:
        print("FOUND END")
        sky.step(-1)
        sky.plot()
        break

    last_width = width
    step += 1

sleep(10)