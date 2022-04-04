import time
time.perf_counter()
from game_mechanics import Player, Simulator
from strategies import make_turn_strat
from grid_plot import imshow_multiplot, imshow_dict
import numpy as np

# 2 bots (Alice and Bob) play against each other.
# Each bot leaves when the turn reaches their individual Turn Threshold value.
# The game is simulated many times for each combination of Turn Threshold values
# within the Turn Threshold ranges for each bot.
# Plots the percentage of games won by the bot for each Turn Threshold value combination.

# Set demo = 1 to see Alice and Bob's win percentage plots with data overlay.
# Set demo = 2 to see Alice and Bob's win, draw and loss percentage plots and average score plots.
demo = 1

# Set the number of simulations per Turn Threshold value combination.
games = 100

# Set the lower and upper values (and step size) for the Turn Threshold range.
alice_lower = 1
alice_upper = 11
bob_lower = 1
bob_upper = 11

# Set whether to print and plot data.
print_data = True
plot_data = True

# Set random seed if desired.
seed = None

# No need to modify below here.
alice_turn_range = list(range(alice_lower, alice_upper))
bob_turn_range = list(range(bob_lower, bob_upper))

alice_win_percent = np.zeros(shape=(alice_upper, bob_upper))
alice_draw_percent = np.zeros(shape=(alice_upper, bob_upper))
alice_loss_percent = np.zeros(shape=(alice_upper, bob_upper))
alice_score_ave = np.zeros(shape=(alice_upper, bob_upper))

bob_win_percent = np.zeros(shape=(alice_upper, bob_upper))
bob_draw_percent = np.zeros(shape=(alice_upper, bob_upper))
bob_loss_percent = np.zeros(shape=(alice_upper, bob_upper))
bob_score_ave = np.zeros(shape=(alice_upper, bob_upper))

for alice_turn_threshold in alice_turn_range:
    alice_turn_strat = make_turn_strat(alice_turn_threshold)

    for bob_turn_threshold in bob_turn_range:
        bob_turn_strat = make_turn_strat(bob_turn_threshold)

        alice = Player("Alice", alice_turn_strat)
        bob = Player("Bob", bob_turn_strat)

        players = [alice, bob]

        incan = Simulator(verbosity=0, manual=False, seed=seed)
        incan.sim(games, players)

        n = len(alice.log)
        alice_win_percent[alice_turn_threshold, bob_turn_threshold] = round(100 * alice.wins / n)
        alice_draw_percent[alice_turn_threshold, bob_turn_threshold] = round(100 * alice.draws / n)
        alice_loss_percent[alice_turn_threshold, bob_turn_threshold] = round(100 * alice.losses / n)
        alice_score_ave[alice_turn_threshold, bob_turn_threshold] = round(sum(alice.log) / n)

        n = len(bob.log)
        bob_win_percent[alice_turn_threshold, bob_turn_threshold] = round(100 * bob.wins / n)
        bob_draw_percent[alice_turn_threshold, bob_turn_threshold] = round(100 * bob.draws / n)
        bob_loss_percent[alice_turn_threshold, bob_turn_threshold] = round(100 * bob.losses / n)
        bob_score_ave[alice_turn_threshold, bob_turn_threshold] = round(sum(bob.log) / n)

generic_dict = {"y_tick_labels": alice_turn_range,
                "x_tick_labels": bob_turn_range,
                "y_label": "Alice's Turn Threshold",
                "x_label": "Bob's Turn Threshold"}

if demo == 1:
    dicts = [imshow_dict(generic_dict, alice_win_percent[alice_lower:, bob_lower:], "Alice's Win Percentage"),
             imshow_dict(generic_dict, bob_win_percent[alice_lower:, bob_lower:], "Bob's Win Percentage")]

if demo == 2:
    dicts = [imshow_dict(generic_dict, alice_win_percent[alice_lower:, bob_lower:], "Alice's Win Percentage"),
             imshow_dict(generic_dict, alice_draw_percent[alice_lower:, bob_lower:], "Alice's Draw Percentage"),
             imshow_dict(generic_dict, alice_loss_percent[alice_lower:, bob_lower:], "Alice's Loss Percentage"),
             imshow_dict(generic_dict, alice_score_ave[alice_lower:, bob_lower:], "Alice's Score Average"),
             imshow_dict(generic_dict, bob_win_percent[alice_lower:, bob_lower:], "Bob's Win Percentage"),
             imshow_dict(generic_dict, bob_draw_percent[alice_lower:, bob_lower:], "Bob's Draw Percentage"),
             imshow_dict(generic_dict, bob_loss_percent[alice_lower:, bob_lower:], "Bob's Loss Percentage"),
             imshow_dict(generic_dict, bob_score_ave[alice_lower:, bob_lower:], "Bob's Score Average")]

if print_data:
    for item in dicts:
        print(item["title"])
        print(item["data"])

print("Program run time (seconds):", time.perf_counter())

if demo == 1:
    imshow_multiplot(dicts, 1, 2, text=True)

if demo == 2:
    imshow_multiplot(dicts, 2, 4, text=False)
