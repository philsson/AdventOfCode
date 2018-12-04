#!/usr/bin/env python
# -*- coding: utf-8 -*-

sum = 0

with open('numlist.txt') as numlist:
    for line in numlist:
        sum += int(line)

print(sum)