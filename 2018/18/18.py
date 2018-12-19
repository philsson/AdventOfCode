#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cProfile
import numpy as np
import time


class Field:

    def __init__(self, map):
        self.map = map

    def step(self):
        (w, h) = self.map.shape
        new_map = np.full((w, h), ' ')

        for y in range(0, h):
            for x in range(0, w):
                unique, counts = np.unique(self.map[max(0, x - 1):min(w, x + 2), max(0, y - 1):min(h, y + 2)], return_counts=True)
                d = dict(zip(unique, counts))

                d[self.map[x, y]] -= 1
                if self.map[x, y] == '.':
                    if '|' in d and d['|'] >= 3:
                        new_map[x, y] = '|'
                    else:
                        new_map[x, y] = self.map[x, y]
                elif self.map[x, y] == '|':
                    if '#' in d and d['#'] >= 3:
                        new_map[x, y] = '#'
                    else:
                        new_map[x, y] = self.map[x, y]
                elif self.map[x, y] == '#':
                    if '|' in d and d['#'] >= 1 and d['|'] >= 1:
                        new_map[x, y] = self.map[x, y]
                    else:
                        new_map[x, y] = '.'

        self.map = new_map

    def print(self):
        self.print_map(self.map)

    @staticmethod
    def print_map(map):
        (w, h) = map.shape

        for y in range(0, h):
            for x in range(0, w):
                print(map[x, y], sep='', end='')
            print()
        print()

    def get_count_of(self, resource):
        unique, counts = np.unique(self.map, return_counts=True)
        d = dict(zip(unique, counts))
        return d[resource]


def parse(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()

    h = len(lines)
    w = len(lines[0].rstrip())

    map = np.full((w, h), ' ')

    y = 0
    for line in lines:
        x = 0
        line = line.rstrip()
        for c in line:
            map[x, y] = c
            x += 1
        y += 1

    return map


def run_a():

    print("A:")

    #field = Field(parse('test_input.txt'))
    field = Field(parse('puzzle_input.txt'))

    field.print()

    for x in range(0, 10):
        field.step()

        field.print()

    print("Lumber:", field.get_count_of('#'))
    print("Trees:", field.get_count_of('|'))
    print("Total resource value:", field.get_count_of('#')*field.get_count_of('|'))
    print()


def run_b():

    print("B:")
    start = time.time()

    field = Field(parse('puzzle_input.txt'))

    p = 0
    #iters = 1000000000
    iters = 100
    for x in range(0, iters):
        field.step()
        if not x % (iters/100):
            print(round(x/iters*100, 2), '%')

    print("Lumber:", field.get_count_of('#'))
    print("Trees:", field.get_count_of('|'))
    print("Total resource value:", field.get_count_of('#')*field.get_count_of('|'))
    print("Finished in", time.time() - start)


# The program
if __name__ == '__main__':

    # open ground (.), trees (|), or a lumberyard (#)

    run_a()

    # B is not performing well enough. Needs optimizing
    # Only running 100 iterations for profiling
    cProfile.run('run_b()')