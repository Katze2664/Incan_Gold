import time
time.perf_counter()
from incan_gold import Player, Simulator
from strategies import make_backpack_strat
import numpy as np
import matplotlib.pyplot as plt

games = 100

lower = 1
upper = 101
step = 3
backpack_range = list(range(lower, upper, step))

score_max = []
score_ave = []
score_std = []
score_min = []

for backpack_threshold in backpack_range:
    backpack_strat = make_backpack_strat(backpack_threshold)
    bot = Player("Bot", backpack_strat)

    players = [bot]

    incan = Simulator(verbose=0, manual=False)
    incan.sim(games, players)

    score_ave.append(sum(bot.log) / len(bot.log))
    score_std.append(np.std(bot.log, ddof=1))
    score_min.append(min(bot.log))
    score_max.append(max(bot.log))

for index, backpack in enumerate(backpack_range):
    print(f"Backpack {backpack}: Ave = {round(score_ave[index], 1)} +/- {round(score_std[index])}")


score_ave_sorted = sorted(zip(score_ave, backpack_range), reverse=True)
print(f"\n1st - Backpack {score_ave_sorted[0][1]}: Ave = {round(score_ave_sorted[0][0], 1)}")
print(f"2nd - Backpack {score_ave_sorted[1][1]}: Ave = {round(score_ave_sorted[1][0], 1)}")
print(f"3rd - Backpack {score_ave_sorted[2][1]}: Ave = {round(score_ave_sorted[2][0], 1)}")

plt.errorbar(backpack_range, score_max, fmt="go-", label="max")
plt.errorbar(backpack_range, score_ave, fmt="bo-", label="average +/- std")
plt.errorbar(backpack_range, score_ave, yerr=score_std, fmt="bo")
plt.errorbar(backpack_range, score_min, fmt="ro-", label="min")
plt.legend()
plt.xticks(backpack_range)
plt.xlabel("Backpack Threshold")
plt.ylabel("Score")
plt.title("Single-player score when waiting for Backpack Threshold")

print("time", time.perf_counter())

plt.show()
