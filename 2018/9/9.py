#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Game():

    def __init__(self):
        self.marbles = [0]
        self.index = 0
        self.progress = 1

    def print_list(self, player):
        p = ("[" + str(player) +  "]")
        print("%-4s" % p, end='')

        for num in self.marbles:
            if num == self.marbles[self.index]:
                f = "(" + str(num) + ")"
            else:
                f = " " + str(num)

            print("%-4s" % f, sep='', end='')
        print("")

    def step_to_pos(self, steps):
        index = (self.index + steps) % len(self.marbles)
        if index == 0:
            return len(self.marbles)
        return index

    def insert_marble(self):
        if self.progress % 23 is 0:
            score = self.progress

            index_to_remove = self.step_to_pos(-7)
            score += self.marbles.pop(index_to_remove)

            self.index = (index_to_remove) % len(self.marbles)

            self.progress += 1
            return score
        else:
            index = self.step_to_pos(2)
            self.marbles.insert(index, self.progress)
            self.progress += 1
            self.index = index

            # Returns the score for this play
            return 0


game = Game()
game.print_list(0)

num_of_players = 0
num_of_marbles = 0

example_set = False

if example_set:
    # Test
    num_of_players = 9
    num_of_marbles = 25
else:
    # The assignment
    num_of_players = 427
    num_of_marbles = 70723

players = {}
for x in range(0, num_of_players + 1):
    players[x] = 0

player = 1
for x in range(0, num_of_marbles):

    players[player] += game.insert_marble()

    if example_set:
        game.print_list(player)

    player += 1
    if player > num_of_players:
        player = 1

max_score = 0
for player, score in players.items():
    if score > max_score:
        max_score = score

print(max_score)
