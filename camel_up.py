from copy import deepcopy
import numpy as np
import sys
import random

sys.setrecursionlimit(15000)


class CamelBoard:

    def __init__(self, board_dict):
        self.colors = ["b", "g", "o", "y", "w"]
        self.N = 16
        self.board = ["" for i in range(self.N)]
        self.rolled = {a: False for a in self.colors}
        self.winner = ""
        self.round_probabilities = None
        self.game_probabilities = None
        for (k, v) in board_dict.items():
            if k > self.N:
                self.winner = v
            else:
                self.board[k - 1] = v

    def add_roll(self, color, roll):
        self.round_probabilities = None
        self.game_probabilities = None
        self.rolled[color] = True
        pos = self.get_position(color)
        if pos == 0:
            self.board[roll - 1] += color
            return False
        fr = pos - 1

        pile = self.board[fr]
        height = pile.find(color)
        bottom = pile[:height]
        top = pile[height:]

        self.board[fr] = bottom

        to = fr + roll
        if to >= self.N:
            self.winner = top
            return True
        if self.board[to] == '-':
            to -= 1
            self.board[to] = top + self.board[to]
        elif self.board[to] == '+':
            to += 1
            if to >= self.N:
                self.winner = top
                return True
            self.board[to] += top
        else:
            self.board[to] += top

        return False

    def add_random_roll(self):
        if all(self.rolled.values()):
            self.rolled = {a: False for a in self.colors}
        possible_colors = [color for color, rolled in self.rolled.items() if not rolled]
        return self.add_roll(random.choice(possible_colors), random.randint(1, 3))

    def get_position(self, color):
        for (i, s) in enumerate(self.board):
            if color in s:
                return i + 1
        return 0

    def get_order_string(self):
        order_string = ""
        for step in self.board:
            if step != '-' and step != '+':
                order_string += step
        order_string += self.winner
        return order_string[::-1]

    def get_order_matrix(self):
        order_string = self.get_order_string()
        order_matrix = np.zeros((len(self.colors), len(self.colors)))
        for (i, color) in enumerate(order_string):
            order_matrix[i, self.colors.index(color)] += 1
        return order_matrix

    def get_round_probabilities(self):
        if self.round_probabilities is None:
            self.compute_round_probabilities()
        return self.round_probabilities

    def get_game_probabilities(self):
        if self.game_probabilities is None:
            self.compute_game_probabilities()
        return self.game_probabilities

    def compute_round_probabilities(self):
        total_order_matrix = np.zeros((len(self.colors), len(self.colors)))
        if all(self.rolled.values()):
            self.round_probabilities = self.get_order_matrix()
            return
        n = list(self.rolled.values()).count(False) * 3
        for color, rolled in self.rolled.items():
            if not rolled:
                for roll in range(1, 4):
                    c = deepcopy(self)
                    finish = c.add_roll(color, roll)
                    if finish:
                        total_order_matrix += c.get_order_matrix()
                    else:
                        total_order_matrix += c.get_round_probabilities()
        self.round_probabilities = total_order_matrix / n

    def compute_game_probabilities(self):
        total_order_matrix = np.zeros((len(self.colors), len(self.colors)))
        import time

        i = 0
        t_start = time.time() + 5
        while time.time() - t_start < 5:
            c = deepcopy(self)
            finished = False
            while not finished:
                finished = c.add_random_roll()
            total_order_matrix += c.get_order_matrix()
            i += 1
        print(f"Simulated {i} games")
        self.game_probabilities = total_order_matrix / i

    def expected_value_of_round_bet(self, win):
        probabilities = self.get_round_probabilities()
        return np.array([win, 1, -1, -1, -1]).dot(probabilities)

    def expected_value_of_game_winner_bet(self, win):
        probabilities = self.get_game_probabilities()
        return np.array([win, -1, -1, -1, -1]).dot(probabilities)

    def expected_value_of_game_loser_bet(self, win):
        probabilities = self.get_game_probabilities()
        return np.array([-1, -1, -1, -1, win]).dot(probabilities)
