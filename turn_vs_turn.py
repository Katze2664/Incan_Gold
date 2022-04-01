from incan_gold import Player, Simulator
from strategies import make_turn_strat
from grid_plot import imshow_plot, imshow_2plots
import numpy as np


games = 10

alice_lower = 4
alice_upper = 11
bob_lower = 4
bob_upper = 11

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

        incan = Simulator(verbose=0, manual=False)
        incan.sim(games, players)

        n = len(alice.log)
        alice_win_percent[alice_turn_threshold, bob_turn_threshold] = round(100 * alice.wins / n, 1)
        alice_draw_percent[alice_turn_threshold, bob_turn_threshold] = round(100 * alice.draws / n, 1)
        alice_loss_percent[alice_turn_threshold, bob_turn_threshold] = round(100 * alice.losses / n, 1)
        alice_score_ave[alice_turn_threshold, bob_turn_threshold] = round(sum(alice.log) / n, 1)

        n = len(bob.log)
        bob_win_percent[alice_turn_threshold, bob_turn_threshold] = round(100 * bob.wins / n, 1)
        bob_draw_percent[alice_turn_threshold, bob_turn_threshold] = round(100 * bob.draws / n, 1)
        bob_loss_percent[alice_turn_threshold, bob_turn_threshold] = round(100 * bob.losses / n, 1)
        bob_score_ave[alice_turn_threshold, bob_turn_threshold] = round(sum(bob.log) / n, 1)

print("alice_win_percent")
print(alice_win_percent)
alice_cropped = alice_win_percent[alice_lower:, bob_lower:]
print(alice_cropped)

print("bob_win_percent")
print(bob_win_percent)
bob_cropped = bob_win_percent[alice_lower:, bob_lower:]
print(bob_cropped)

imshow_2plots(alice_cropped,
              alice_turn_range,
              bob_turn_range,
              "Alice's Turn Threshold",
              "Bob's Turn Threshold",
              "Alice's Win Percentage",
              bob_cropped,
              alice_turn_range,
              bob_turn_range,
              "Alice's Turn Threshold",
              "Bob's Turn Threshold",
              "Bob's Win Percentage")





# fig, ax = plt.subplots()
# im = ax.imshow(alice_win_percent[alice_lower:, bob_lower:])
#
# ax.set_yticks(np.arange(len(alice_turn_range)), labels=alice_turn_range)
# ax.set_xticks(np.arange(len(bob_turn_range)), labels=bob_turn_range)
#
# for y in np.arange(len(alice_turn_range)):
#     for x in np.arange(len(bob_turn_range)):
#         ax.text(x, y, alice_cropped[y, x], ha="center", va="center", color="w")
#
# ax.set_title("Alice's Win Percentage")
# ax.set_ylabel("Alice's Turn Threshold")
# ax.set_xlabel("Bob's Turn Threshold")
# fig.tight_layout()
# plt.show()

# print("alice_draw_percent")
# print(alice_draw_percent)
# print("alice_loss_percent")
# print(alice_loss_percent)
# print("alice_score_ave")
# print(alice_score_ave)
#
#
# print("bob_win_percent")
# print(bob_win_percent)
# print("bob_draw_percent")
# print(bob_draw_percent)
# print("bob_loss_percent")
# print(bob_loss_percent)
# print("bob_score_ave")
# print(bob_score_ave)







# for index, turn in enumerate(turn_range):
#     print(f"Turns {turn}: Ave = {round(score_ave[index], 1)} +/- {round(score_std[index])}")
#
# score_ave_sorted = sorted(zip(score_ave, turn_range), reverse=True)
# print(f"\n1st - Turns {score_ave_sorted[0][1]}: Ave = {round(score_ave_sorted[0][0], 1)}")
# print(f"2nd - Turns {score_ave_sorted[1][1]}: Ave = {round(score_ave_sorted[1][0], 1)}")
# print(f"3rd - Turns {score_ave_sorted[2][1]}: Ave = {round(score_ave_sorted[2][0], 1)}")
#
# plt.errorbar(turn_range, score_max, fmt="go-", label="max")
# plt.errorbar(turn_range, score_ave, fmt="bo-", label="average +/- std")
# plt.errorbar(turn_range, score_ave, yerr=score_std, fmt="bo")
# plt.errorbar(turn_range, score_min, fmt="ro-", label="min")
# plt.legend()
# plt.xticks(turn_range)
# plt.xlabel("Turn Threshold")
# plt.ylabel("Score")
# plt.title("Single-player score when waiting for Turn Threshold")
# plt.show()
