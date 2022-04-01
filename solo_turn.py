from incan_gold import Player, Simulator
from strategies import make_turn_strat
import numpy as np
import matplotlib.pyplot as plt

games = 1000

lower = 1
upper = 21
turn_range = list(range(lower, upper))

score_max = []
score_ave = []
score_std = []
score_min = []

for turn_threshold in turn_range:
    turn_strat = make_turn_strat(turn_threshold)
    bot = Player("Bot", turn_strat)

    players = [bot]

    incan = Simulator(verbose=0, manual=False)
    incan.sim(games, players)

    score_ave.append(sum(bot.log) / len(bot.log))
    score_std.append(np.std(bot.log, ddof=1))
    score_min.append(min(bot.log))
    score_max.append(max(bot.log))

for index, turn in enumerate(turn_range):
    print(f"Turns {turn}: Ave = {round(score_ave[index], 1)} +/- {round(score_std[index])}")

score_ave_sorted = sorted(zip(score_ave, turn_range), reverse=True)
print(f"\n1st - Turns {score_ave_sorted[0][1]}: Ave = {round(score_ave_sorted[0][0], 1)}")
print(f"2nd - Turns {score_ave_sorted[1][1]}: Ave = {round(score_ave_sorted[1][0], 1)}")
print(f"3rd - Turns {score_ave_sorted[2][1]}: Ave = {round(score_ave_sorted[2][0], 1)}")

plt.errorbar(turn_range, score_max, fmt="go-", label="max")
plt.errorbar(turn_range, score_ave, fmt="bo-", label="average +/- std")
plt.errorbar(turn_range, score_ave, yerr=score_std, fmt="bo")
plt.errorbar(turn_range, score_min, fmt="ro-", label="min")
plt.legend()
plt.xticks(turn_range)
plt.xlabel("Turn Threshold")
plt.ylabel("Score")
plt.title("Single-player score when waiting for Turn Threshold")
plt.show()
