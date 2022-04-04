import time
time.perf_counter()
from game_mechanics import Player, Simulator
from strategies import make_backpack_strat
import numpy as np
import matplotlib.pyplot as plt

# A bot plays Incan Gold in single-player mode.
# The bot leaves when the reaches or exceeds the Backpack Threshold value.
# The game is simulated many times for a range of Backpack Threshold values.
# Plots the average score achieved by the bot for each Backpack Threshold value.

# Set the number of simulations per Backpack Threshold value.
games = 100

# Set the lower and upper values (and step size) for the Backpack Threshold range.
lower = 1
upper = 101
step = 3

# Set whether to print and plot data.
print_data = True
print_best = True
plot_data = True

# Set random seed if desired.
seed = None

# No need to modify below here.
backpack_range = list(range(lower, upper, step))

score_max = []
score_ave = []
score_std = []
score_min = []

for backpack_threshold in backpack_range:
    backpack_strat = make_backpack_strat(backpack_threshold)
    bot = Player("Bot", backpack_strat)

    players = [bot]

    incan = Simulator(verbosity=0, manual=False, seed=seed)
    incan.sim(games, players)

    score_ave.append(sum(bot.log) / len(bot.log))
    score_std.append(np.std(bot.log, ddof=1))
    score_min.append(min(bot.log))
    score_max.append(max(bot.log))

if print_data:
    for index, backpack in enumerate(backpack_range):
        print(f"Backpack {backpack}: Ave = {round(score_ave[index], 1)} +/- {round(score_std[index])}")

if print_best:
    score_ave_sorted = sorted(zip(score_ave, backpack_range), reverse=True)
    print("\nHighest scoring Backpack Threshold values:")
    print(f"1st - Backpack {score_ave_sorted[0][1]}: Ave = {round(score_ave_sorted[0][0], 1)}")
    print(f"2nd - Backpack {score_ave_sorted[1][1]}: Ave = {round(score_ave_sorted[1][0], 1)}")
    print(f"3rd - Backpack {score_ave_sorted[2][1]}: Ave = {round(score_ave_sorted[2][0], 1)}")

if plot_data:
    plt.errorbar(backpack_range, score_max, fmt="go-", label="max")
    plt.errorbar(backpack_range, score_ave, fmt="bo-", label="average +/- std")
    plt.errorbar(backpack_range, score_ave, yerr=score_std, fmt="bo")
    plt.errorbar(backpack_range, score_min, fmt="ro-", label="min")
    plt.legend()
    plt.xticks(backpack_range)
    plt.xlabel("Backpack Threshold")
    plt.ylabel("Score")
    plt.title("Single-player score when waiting for Backpack Threshold")

print("Program run time (seconds):", time.perf_counter())

if plot_data:
    plt.show()
