#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sortedcontainers import SortedList

sum = 0

list = SortedList()

condition = True
counter = 0

with open('numlist.txt') as numlist:

    while condition:
        for line in numlist:
            sum += int(line)
            if list.__contains__(sum):
                print("found:", sum)
                condition = False
                break
            list.add(sum)
        numlist.seek(0) #Return to beginning of file
