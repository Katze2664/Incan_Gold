import time
time.perf_counter()
from game_mechanics import Player, Simulator
from strategies import make_random_strat
import numpy as np
import matplotlib.pyplot as plt

# A bot plays Incan Gold in single-player mode.
# The bot leaves when with a probability of Random Threshold each turn.
# The game is simulated many times for a range of Random Threshold values.
# Plots the average score achieved by the bot for each Random Threshold value.

# Set the number of simulations per Random Threshold value.
games = 100

# Set the lower and upper values (and step size) for the Random Threshold range (in percent).
lower = 5
upper = 101
step = 5

# Set whether to print and plot data.
print_data = True
print_best = True
plot_data = True

# Set random seed if desired.
seed = None

# No need to modify below here.
random_range = [i/100 for i in range(lower, upper, step)]

score_max = []
score_ave = []
score_std = []
score_min = []

for random_threshold in random_range:
    random_strat = make_random_strat(random_threshold)
    bot = Player("Bot", random_strat)

    players = [bot]

    incan = Simulator(verbosity=0, manual=False, seed=seed)
    incan.sim(games, players)

    score_ave.append(sum(bot.log) / len(bot.log))
    score_std.append(np.std(bot.log, ddof=1))
    score_min.append(min(bot.log))
    score_max.append(max(bot.log))

if print_data:
    for index, random in enumerate(random_range):
        print(f"Random {random}: Ave = {round(score_ave[index], 1)} +/- {round(score_std[index])}")

if print_best:
    score_ave_sorted = sorted(zip(score_ave, random_range), reverse=True)
    print("\nHighest scoring Random Threshold values:")
    print(f"1st - Random {score_ave_sorted[0][1]}: Ave = {round(score_ave_sorted[0][0], 1)}")
    print(f"2nd - Random {score_ave_sorted[1][1]}: Ave = {round(score_ave_sorted[1][0], 1)}")
    print(f"3rd - Random {score_ave_sorted[2][1]}: Ave = {round(score_ave_sorted[2][0], 1)}")

if plot_data:
    plt.errorbar(random_range, score_max, fmt="go-", label="max")
    plt.errorbar(random_range, score_ave, fmt="bo-", label="average +/- std")
    plt.errorbar(random_range, score_ave, yerr=score_std, fmt="bo")
    plt.errorbar(random_range, score_min, fmt="ro-", label="min")
    plt.legend()
    plt.xticks(random_range)
    plt.xlabel("Random Threshold")
    plt.ylabel("Score")
    plt.title("Single-player score when leaving with probabily = Random Threshold")

print("Program run time (seconds):", time.perf_counter())

if plot_data:
    plt.show()
