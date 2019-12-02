#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy


def compute(nums, noun=12, verb=2):

    nums[1] = noun
    nums[2] = verb

    x = 0
    while x < len(nums):
        if nums[x] == 1:
            nums[nums[x + 3]] = nums[nums[x + 1]] + nums[nums[x + 2]]
            x += 4
        elif nums[x] == 2:
            nums[nums[x + 3]] = nums[nums[x + 1]] * nums[nums[x + 2]]
            x += 4
        elif nums[x] == 99:
            #print("Program End")
            return nums[0]


def find_target(nums, target: int):
    for noun in range(0, 99):
        for verb in range(0, 99):
            if compute(copy.deepcopy(nums), noun, verb) == target:
                print("noun {} and verb {}. \n100 * noun + verb is {}".format(noun, verb, 100 * noun + verb))
                return


if __name__ == '__main__':
    f = open('puzzle_input.txt', 'r')
    nums = [int(x) for x in f.readlines()[0].split(',')]
    f.close()

    print("A:\n{}".format(compute(copy.deepcopy(nums))))

    print("\nB:")
    find_target(nums, 19690720)





