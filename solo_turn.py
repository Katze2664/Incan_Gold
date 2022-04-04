import time
time.perf_counter()

from game_mechanics import Player, Simulator
from strategies import make_turn_strat
import numpy as np
import matplotlib.pyplot as plt

# A bot plays Incan Gold in single-player mode.
# The bot leaves when the turn reaches the Turn Threshold value.
# The game is simulated many times for a range of Turn Threshold values.
# Plots the average score achieved by the bot for each Turn Threshold value.

# Set the number of simulations per Turn Threshold value.
games = 1000

# Set the lower and upper values (and step size) for the Turn Threshold range.
lower = 1
upper = 21
step = 1

# Set whether to print and plot data.
print_data = True
print_best = True
plot_data = True

# Set random seed if desired.
seed = None

# No need to modify below here.
turn_range = list(range(lower, upper, step))

score_max = []
score_ave = []
score_std = []
score_min = []

for turn_threshold in turn_range:
    turn_strat = make_turn_strat(turn_threshold)
    bot = Player("Bot", turn_strat)

    players = [bot]

    incan = Simulator(verbosity=0, manual=False, seed=seed)
    incan.sim(games, players)

    score_ave.append(sum(bot.log) / len(bot.log))
    score_std.append(np.std(bot.log, ddof=1))
    score_min.append(min(bot.log))
    score_max.append(max(bot.log))

if print_data:
    for index, turn in enumerate(turn_range):
        print(f"Turns {turn}: Ave = {round(score_ave[index], 1)} +/- {round(score_std[index])}")

if print_best:
    score_ave_sorted = sorted(zip(score_ave, turn_range), reverse=True)
    print("\nHighest scoring Turn Threshold values:")
    print(f"1st - Turns {score_ave_sorted[0][1]}: Ave = {round(score_ave_sorted[0][0], 1)}")
    print(f"2nd - Turns {score_ave_sorted[1][1]}: Ave = {round(score_ave_sorted[1][0], 1)}")
    print(f"3rd - Turns {score_ave_sorted[2][1]}: Ave = {round(score_ave_sorted[2][0], 1)}")

if plot_data:
    plt.errorbar(turn_range, score_max, fmt="go-", label="max")
    plt.errorbar(turn_range, score_ave, fmt="bo-", label="average +/- std")
    plt.errorbar(turn_range, score_ave, yerr=score_std, fmt="bo")
    plt.errorbar(turn_range, score_min, fmt="ro-", label="min")
    plt.legend()
    plt.xticks(turn_range)
    plt.xlabel("Turn Threshold")
    plt.ylabel("Score")
    plt.title("Single-player score when waiting for Turn Threshold")

print("Program run time (seconds):", time.perf_counter())

if plot_data:
    plt.show()
