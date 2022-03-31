from incan_gold import Player, Simulator
from strategies import make_turn_strat
import numpy as np
import matplotlib.pyplot as plt

games = 1000

lower = 1
upper = 20
turns = list(range(lower, upper + 1))

score_max = []
score_ave = []
score_std = []
score_min = []

for i in turns:
    turn_strat = make_turn_strat(i)
    bot = Player("Bot", turn_strat)

    players = [bot]

    incan = Simulator(verbose=0, manual=False)
    incan.sim(games, players)

    score_ave.append(sum(bot.log) / len(bot.log))
    score_std.append(np.std(bot.log, ddof=1))
    score_min.append(min(bot.log))
    score_max.append(max(bot.log))

for index, turn in enumerate(turns):
    print(f"Turns {turn}: Ave = {round(score_ave[index], 1)} +/- {round(score_std[index])}")

plt.errorbar(turns, score_max, fmt="go-", label="max")
plt.errorbar(turns, score_ave, fmt="bo-", label="average +/- std")
plt.errorbar(turns, score_ave, yerr=score_std, fmt="bo")
plt.errorbar(turns, score_min, fmt="ro-", label="min")
plt.legend()
plt.xticks(turns)
plt.xlabel("Turns")
plt.ylabel("Score")
plt.title("Single-player score when leaving on Turn x")
plt.show()
