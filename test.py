import numpy as np
from camel_up import CamelBoard

np.set_printoptions(precision=2)
x = CamelBoard({1: "y", 2: "", 3: "gbo", 4: "w", 5: "-"})
print(x.board)

print("Computing round probabilities:")
round_probabilities = x.get_round_probabilities()
print(x.colors)
print(round_probabilities)
print("Expected value of round bet:")
print(x.colors)
for win in [5, 3, 2]:
    print(win, x.expected_value_of_round_bet(win))

print("Computing game probabilities:")
game_probabilities = x.get_game_probabilities()
print(x.colors)
print(game_probabilities)
print("Expected value of game winner bet:")
print(x.colors)
for win in [8, 5, 3, 2, 1]:
    print(win, x.expected_value_of_game_winner_bet(win))
print("Expected value of game loser bet:")
print(x.colors)
for win in [8, 5, 3, 2, 1]:
    print(win, x.expected_value_of_game_loser_bet(win))
