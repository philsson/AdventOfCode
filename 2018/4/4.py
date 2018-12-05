#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy
import numpy as np
import operator


class Time(object):

    def __init__(self):
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.minute = 0

    def __eq__(self, other):
        return self.year == other.year \
               and self.month == other.month \
               and self.day == other.day \
               and self.hour == other.hour \
               and self.minute == other.minute

    def __lt__(self, other):
        if self.year != other.year:
            return self.year < other.year
        if self.month != other.month:
            return self.month < other.month
        if self.day != other.day:
            return self.day < other.day
        if self.hour != other.hour:
            return self.hour < other.hour
        return self.minute < other.minute

class Shift(object):

    def __init__(self):
        self.guard = None
        self.start = Time()
        self.falls_asleep = Time()
        self.wakes_up = Time()


class Event(object):

    def __init__(self, string):
        self.time = Time()
        str1, self.event = string.replace("[", "").split(']')
        #print(str1)
        str_date, str_time = str1.split(' ')
        self.time.year, self.time.month, self.time.day = \
            (int(x) for x in str_date.split('-'))
        self.time.hour, self.time.minute = (int(x) for x in str_time.split(':'))
        #print(str2)

    def __eq__(self, other):
        return self.time == other.time

    def __lt__(self, other):
        return self.time < other.time


class Guard(object):

    def __init__(self, id, sleep):
        self.id = id
        self.score = 0
        self.sleep = sleep
        self.max_index = -1

    def update_score(self):
        max_index = self.sleep.argmax()
        #print("Max index:", max_index, "Value:", self.sleep[0, max_index])
        self.score = max_index * self.id
        self.max_index = max_index

    def append_sleep(self, sleep):
        self.sleep += sleep
        self.update_score()
        #print("Appending to Guard", self.id)
        #print(self.sleep)
        #print("score: ", self.score)

    def __eq__(self, other):
        return self.score == other.score

    def __lt__(self, other):
        return self.score < other.score


def print_time(time):
    print(time.year, "-", str(time.month).zfill(2),
          "-", str(time.day).zfill(2),
          " ", str(time.hour).zfill(2), ":",
          str(time.minute).zfill(2), sep='')

def print_event(event):
    print_time(event.time)
    print(event.event)

def print_shift(shift):
    print("Guard", shift.guard, "shift:")
    print_time(shift.start)
    print_time(shift.falls_asleep)
    print_time(shift.wakes_up)

def parse_eventlist():
    f = open('puzzle_input.txt', 'r')
    unordered_string_list = f.readlines()
    f.close()

    unordered_event_list = []
    for p in unordered_string_list:
        unordered_event_list.append(Event(p))
        #print_event(Event(p))
    return unordered_event_list


unordered_event_list = parse_eventlist()

sorted_event_list = sorted(unordered_event_list)

current_guard = None

shift = Shift()
shifts = []
guards = {}
for event in sorted_event_list:
    if "Guard" in event.event:
        shift.guard = int(event.event.replace("#", "").split(' ')[2])
        shift.start = event.time
    if "asleep" in event.event:
        shift.falls_asleep = event.time
    if "wakes" in event.event:
        shift.wakes_up = event.time
        shifts.append(deepcopy(shift))

        sleep = np.zeros((1, 60))
        sleep[0, shift.falls_asleep.minute:shift.wakes_up.minute] = 1
        if shift.guard in guards:
            guards[shift.guard].append_sleep(sleep)
        else:
            guards[shift.guard] = Guard(shift.guard, sleep)
        #print_shift(shift)
    #print_event(event)

sorted_guards = sorted(guards.items(), key=operator.itemgetter(1))
highest_score = 0
max_value = -1
max_index = None
max_index_guard = None
for key, value in sorted_guards:
    if value.score > highest_score:
        highest_score = value.score
    if value.sleep[0, value.max_index] > max_value:
        max_value = value.sleep[0, value.max_index]
        max_index_guard = key
        max_index = value.max_index
    #print("ID: ", value.id, "Score: ", value.score)
print("A:", highest_score)

print("B:", max_index * max_index_guard)

