#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import multiprocessing, logging
import time

logging.basicConfig(level=logging.DEBUG)
_L = logging.getLogger()


class JobTimeoutException(Exception):
    def __init__(self, jobstack=[]):
        super(JobTimeoutException, self).__init__()
        self.jobstack = jobstack

class ABC:

    def __init__(self, power, x, y, dim):
        self.power = power
        self.x = x
        self.y = y
        self.dim = dim


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

        return ABC(max_power, x_max, y_max, square_size)

    def find_max_block_any_size(self):
        w, h = self.m.shape

        num_of_threads = 10
        pool = multiprocessing.Pool(processes=num_of_threads)  # start 4 worker processes


        print("Working through dimensions with", num_of_threads, "threads...")
        result_iter = pool.imap_unordered(self.find_maximized_block, range(1, w + 1))

        results = []

        try:
            while True:
                try:
                    result = result_iter.next(timeout=99999999)
                    #_L.info("Result received %s", result)
                    results.append(result)
                except JobTimeoutException as timeout_ex:
                    _L.warning("Job timed out %s", timeout_ex)
                    results.append(None)

        except StopIteration:
            _L.info("All jobs complete!")
            pass

        x_max, y_max, dim = 0, 0, 0
        max_power = 0

        for result in results:
            if result.power > max_power:
                max_power = result.power
                x_max, y_max = result.x, result.y
                dim = result.dim

        return max_power, x_max, y_max, dim


# The program
if __name__ == '__main__':

    serial_nr = 5235
    device = WristDevice(serial_nr)

    start = time.time()
    result = device.find_maximized_block()
    print("A: power", result.power, "at x", result.x, "y", result.y)
    print("Finished in", time.time() - start)

    start = time.time()
    max_power, x, y, dim = device.find_max_block_any_size()
    print("B: power", max_power, "at x", x, "y", y, "and power", dim)
    print("Finished in", time.time() - start)