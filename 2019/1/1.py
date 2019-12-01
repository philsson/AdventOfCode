#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math


def calc_fuel(mass: int, recurse: bool) -> int:
    fuel = 0
    while True:
        mass = max(math.floor(mass / 3) - 2, 0)
        fuel += mass
        if mass == 0 or recurse is not True:
            return fuel


if __name__ == '__main__':

    fuel_a, fuel_b = 0, 0

    with open('puzzle_input.txt') as puzzle:
        for line in puzzle:
            fuel_a += calc_fuel(int(line), False)
            fuel_b += calc_fuel(int(line), True)
        print("A: The fuel needed will be {}".format(fuel_a))
        print("B: The fuel needed will be {}".format(fuel_b))


