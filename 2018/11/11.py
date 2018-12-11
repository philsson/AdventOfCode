#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np


class WristDevice:

    def __init__(self, serial_nr):
        self.m = np.zeros((300, 300), dtype=int)
        self.serial_nr = serial_nr
        self.calc_power_levels()

    def set_sn(self, serial_nr):
        self.serial_nr = serial_nr
        self.calc_power_levels()

    def calc_power_levels(self):
        w, h = self.m.shape
        max_power, x, y = 0, 0, 0
        # x and y should be index 1..300
        # 1) (((x + 10) * y) + s) * (x + 10)
        # 2) extract the "hundred" digit
        # 3) subtract by 5. Resulting in the power level

        for x in range(0, w):
            for y in range(0, h):
                rank_id = (x+1) + 10
                power_level = rank_id*(y+1) + self.serial_nr
                power_level = power_level*rank_id
                self.m[x, y] = ((power_level // 100) % 10) - 5

    def get_cell_power(self, x, y):
        return self.m[x - 1, y - 1]

    def get_block_power(self, x, y, square_size=3):
        return self.m[x - 1:x + square_size - 1, y - 1:y + square_size - 1].sum()

    def find_maximized_block(self, square_size=3):
        w, h = self.m.shape

        x_max, y_max = 0, 0
        max_power = 0

        for x in range(1, w + 2 - square_size):
            for y in range(1, h + 2 - square_size):
                power = self.get_block_power(x, y, square_size)
                if power > max_power:
                    max_power = power
                    x_max, y_max = x, y

        return max_power, x_max, y_max

    def find_max_block_any_size(self):
        w, h = self.m.shape

        x_max, y_max, dim = 0, 0, 0
        max_power = 0

        print("Working through dimensions...")
        for x in range(1, w + 1):
            power, x_o, y_o = self.find_maximized_block(x)
            if power > max_power:
                max_power = power
                x_max, y_max = x_o, y_o
                dim = x

        return max_power, x_max, y_max, dim


# The program

serial_nr = 5235
device = WristDevice(serial_nr)

max_power, x, y = device.find_maximized_block()
print("A: power", max_power, "at x", x, "y", y)

max_power, x, y, dim = device.find_max_block_any_size()
print("B: power", max_power, "at x", x, "y", y, "and power", max_power)