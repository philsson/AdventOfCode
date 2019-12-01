#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math


def calc_fuel(mass: int) -> int:
    fuel = math.floor(mass / 3) - 2
    return max(fuel, 0)


def calc_fuel_for_fuel(mass: int) -> int:
    fuel = 0
    while True:
        mass = calc_fuel(mass)
        if mass == 0:
            return fuel
        else:
            fuel += mass


if __name__ == '__main__':

    fuel_a, fuel_b = 0, 0

    with open('puzzle_input.txt') as puzzle:
        for line in puzzle:
            fuel_a += calc_fuel(int(line))
            fuel_b += calc_fuel_for_fuel(int(line))
        print("A: The fuel needed will be {}".format(fuel_a))
        print("B: The fuel needed will be {}".format(fuel_b))


