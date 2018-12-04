#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

pairs = np.matrix('0 0')  # 2s and 3s

def count_letters(box, pairs):
    my_dict = {}
    twos = 0
    threes = 0
    for letter in box:
        if my_dict.get(letter) is not None:
            my_dict[letter] += 1
        else:
            my_dict[letter] = 1
    print(box)
    for item in my_dict.items():
        if item[1] == 2:
            twos = 1
        elif item[1] == 3:
            threes = 1
    pairs[0, 0] += twos
    pairs[0, 1] += threes

with open('boxes.txt') as boxes:
    for box in boxes:
        count_letters(box, pairs)
    print(pairs[0, 0]*pairs[0, 1])
