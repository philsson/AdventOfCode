#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Result of test_input is dabCBAcaDA

from copy import deepcopy
from string import ascii_lowercase


def reaction(molecule1, molecule2):
    if abs(ord(molecule1) - ord(molecule2)) == 32:
        return True
    return False


def remove_molecule_type(charlist, molecule):
    charlist_len = len(charlist)
    x = 0
    while x < charlist_len:
        if charlist[x] == molecule.lower() \
           or charlist[x] == molecule.upper():
            charlist.pop(x)
            charlist_len -= 1
        else:
            x += 1


def start_reaction(charlist):
    charlist_len = len(charlist)

    x = 0
    while x < charlist_len - 1:
        # print(x)
        if reaction(charlist[x], charlist[x + 1]):
            charlist.pop(x + 1)
            charlist.pop(x)
            charlist_len -= 2
            x = x - 1
            x = 0 if x < 0 else x
        else:
            x += 1

    return len(charlist)

#f = open('test_input.txt', 'r')
f = open('puzzle_input.txt', 'r')
strings = f.readlines()
f.close()

string = strings[0]

string_size = len(string)

charlist = list(string)

charlist2 = deepcopy(charlist)

print("A:", start_reaction(charlist))

# Part B

lowest = len(charlist2)
for c in ascii_lowercase:
    charlist3 = deepcopy(charlist2)
    remove_molecule_type(charlist3, c)
    result = start_reaction(charlist3)
    if result < lowest:
        lowest = result
    #print(c, result)
print("B:", lowest)