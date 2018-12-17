#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from copy import deepcopy


class Worker:

    def __init__(self, x, y, dir):
        self.x = x
        self.y = y
        self.dir = dir
        self.last_turn = 0
        self.collided = False

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        if self.y < other.y:
            return True
        elif self.x < other.x:
            return True
        return False

    def turn(self):
        if self.dir == '<':
            if self.last_turn == 0:
                self.dir = 'v'
            elif self.last_turn == 1:
                self.dir = '<'
            elif self.last_turn == 2:
                self.dir = '^'
        elif self.dir == '^':
            if self.last_turn == 0:
                self.dir = '<'
            elif self.last_turn == 1:
                self.dir = '^'
            elif self.last_turn == 2:
                self.dir = '>'
        elif self.dir == '>':
            if self.last_turn == 0:
                self.dir = '^'
            elif self.last_turn == 1:
                self.dir = '>'
            elif self.last_turn == 2:
                self.dir = 'v'
        elif self.dir == 'v':
            if self.last_turn == 0:
                self.dir = '>'
            elif self.last_turn == 1:
                self.dir = 'v'
            elif self.last_turn == 2:
                self.dir = '<'
        self.last_turn += 1
        self.last_turn = self.last_turn % 3

class World:

    def __init__(self):
        self.map = None
        self.workers = []
        self.time = 0

    def print(self):
        temp_map = deepcopy(self.map)
        for worker in self.workers:
            temp_map[worker.x, worker.y] = worker.dir

        w, h = temp_map.shape
        for y in range(0, h):
            for x in range(0, w):
                print(temp_map[x, y], sep='', end='')
            print()

    def advance(self):
        self.time += 1
        self.workers.sort()
        for worker in self.workers:
            if worker.dir is '<':
                if self.map[worker.x - 1, worker.y] == '+':
                    worker.turn()
                elif self.map[worker.x - 1, worker.y] == '/':
                    worker.dir = 'v'
                elif self.map[worker.x - 1, worker.y] == '\\':
                    worker.dir = '^'
                worker.x -= 1
            elif worker.dir is '>':
                if self.map[worker.x + 1, worker.y] == '+':
                    worker.turn()
                elif self.map[worker.x + 1, worker.y] == '\\':
                    worker.dir = 'v'
                elif self.map[worker.x + 1, worker.y] == '/':
                    worker.dir = '^'
                worker.x += 1
            elif worker.dir is '^':
                if self.map[worker.x, worker.y - 1] == '+':
                    worker.turn()
                elif self.map[worker.x, worker.y - 1] == '/':
                    worker.dir = '>'
                elif self.map[worker.x, worker.y - 1] == '\\':
                    worker.dir = '<'
                worker.y -= 1
            elif worker.dir is 'v':
                if self.map[worker.x, worker.y + 1] == '+':
                    worker.turn()
                elif self.map[worker.x, worker.y + 1] == '\\':
                    worker.dir = '>'
                elif self.map[worker.x, worker.y + 1] == '/':
                    worker.dir = '<'
                worker.y += 1

            if self.workers.count(worker) > 1:
                x, y = worker.x - 1, worker.y
                matches = (n for n in self.workers if n == worker)
                for m in matches:
                    m.collided = True
                return self.time, x, y

        # Doing this twice should be considered a bug. TODO: Fix!
        for c in self.workers:
            if c.collided:
                self.workers.remove(c)
        for c in self.workers:
            if c.collided:
                self.workers.remove(c)

        return None, None, None


def parse():
    #f = open('test_input.txt', 'r')
    #f = open('test_input2.txt', 'r')
    #f = open('test_input3.txt', 'r')
    f = open('puzzle_input.txt', 'r')
    map_lines = f.readlines()
    f.close()

    max_length = 0
    for line in map_lines:
        if len(line) + 1 > max_length:
            max_length = len(line) + 1

    world = World()

    map = np.full((max_length, len(map_lines)), ' ')
    y = 0
    for line in map_lines:
        x = 0
        for c in line.rstrip():
            if c in ['<', '>', '^', 'v']:
                worker = Worker(x + 1, y, c)
                if c is '<' or c is '>':
                    map[x + 1, y] = '-'
                elif c is '^' or c is 'v':
                    map[x + 1, y] = '|'
                world.workers.append(worker)
            else:
                map[x + 1, y] = c
            x += 1
        y += 1

    world.map = map

    return world


if __name__ == '__main__':

    worldA = parse()

    #world.print()
    while True:
        time, x, y = worldA.advance()
        if x is not None:
            print("collision!! at time:", time)
            print("and location", x, ",", y)
            break
        #world.print()

    #world.print()
    worldB = parse()
    while True:
        worldB.advance()
        if len(worldB.workers) == 1:

            print("Finish!", worldB.workers[0].x - 1, worldB.workers[0].y)
            break
        #world.print()
    #world.print()