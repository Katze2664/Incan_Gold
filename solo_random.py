import time
time.perf_counter()
from incan_gold import Player, Simulator
from strategies import make_random_strat
import numpy as np
import matplotlib.pyplot as plt

games = 100

lower = 1
upper = 101
step = 3
random_range = [i/100 for i in range(lower, upper, step)]

score_max = []
score_ave = []
score_std = []
score_min = []

for random_threshold in random_range:
    random_strat = make_random_strat(random_threshold)
    bot = Player("Bot", random_strat)

    players = [bot]

    incan = Simulator(verbose=0, manual=False)
    incan.sim(games, players)

    score_ave.append(sum(bot.log) / len(bot.log))
    score_std.append(np.std(bot.log, ddof=1))
    score_min.append(min(bot.log))
    score_max.append(max(bot.log))

for index, random in enumerate(random_range):
    print(f"Random {random}: Ave = {round(score_ave[index], 1)} +/- {round(score_std[index])}")


score_ave_sorted = sorted(zip(score_ave, random_range), reverse=True)
print(f"\n1st - Random {score_ave_sorted[0][1]}: Ave = {round(score_ave_sorted[0][0], 1)}")
print(f"2nd - Random {score_ave_sorted[1][1]}: Ave = {round(score_ave_sorted[1][0], 1)}")
print(f"3rd - Random {score_ave_sorted[2][1]}: Ave = {round(score_ave_sorted[2][0], 1)}")

plt.errorbar(random_range, score_max, fmt="go-", label="max")
plt.errorbar(random_range, score_ave, fmt="bo-", label="average +/- std")
plt.errorbar(random_range, score_ave, yerr=score_std, fmt="bo")
plt.errorbar(random_range, score_min, fmt="ro-", label="min")
plt.legend()
plt.xticks(random_range)
plt.xlabel("Random Threshold")
plt.ylabel("Score")
plt.title("Single-player score when leaving with probabily = Random Threshold")

print("time", time.perf_counter())

plt.show()
