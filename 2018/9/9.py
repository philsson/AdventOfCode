#!/usr/bin/env python
# -*- coding: utf-8 -*-
from blist import *


class Game():

    def __init__(self):
        self.marbles = blist([0])
        self.index = 0
        self.progress = 1
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


def play_game(part):
    print(part, ": ", end='')
    game = Game()

    num_of_players = 427
    num_of_marbles = 70723

    if part is 'B':
        num_of_marbles *= 100

    players = {}
    for x in range(0, num_of_players + 1):
        players[x] = 0

    player = 1
    for x in range(0, num_of_marbles):

        players[player] += game.insert_marble()

        player += 1
        if player > num_of_players:
            player = 1

    max_score = 0
    for player, score in players.items():
        if score > max_score:
            max_score = score

    print(max_score)


# The program
if __name__ == '__main__':
    play_game('A')
    play_game('B')