#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Node(object):

    def __init__(self):
        self.nr_of_children = 0
        self.nr_of_metadata_entries = 0
        self.children = []
        self.metadata_entries = []


def node_creator(nums):

    node = Node()
    node.nr_of_children = nums.pop(0)
    node.nr_of_metadata_entries = nums.pop(0)

    if node.nr_of_children is not 0:
        for x in range(0, node.nr_of_children):
            node.children.append(node_creator(nums))

    if node.nr_of_metadata_entries is not 0:
        for x in range(0, node.nr_of_metadata_entries):
            node.metadata_entries.append(nums.pop(0))

    return node


def count_metadata(node: Node):

    sum = 0

    for child in node.children:
        sum += count_metadata(child)

    for meta in node.metadata_entries:
        sum += meta

    return sum


def calc_value(node: Node):

    value = 0

    if node.nr_of_children is 0:
        for meta in node.metadata_entries:
            value += meta
    else:
        for meta in node.metadata_entries:
            if meta <= node.nr_of_children:
                value += calc_value(node.children[meta - 1])

    return value


#f = open('test_input.txt', 'r')
f = open('puzzle_input.txt', 'r')
lines = f.readlines()
f.close()

nums = (int(x) for x in lines[0].split(' '))
numbers = []
for x in nums:
    numbers.append(x)

root_node = node_creator(numbers)

print("A:", count_metadata(root_node))

print("B:", calc_value(root_node))



