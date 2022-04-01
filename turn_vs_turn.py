import time
time.perf_counter()
from incan_gold import Player, Simulator
from strategies import make_turn_strat
from grid_plot import imshow_multiplot, imshow_dict
import numpy as np

games = 100

alice_lower = 1
alice_upper = 11
bob_lower = 1
bob_upper = 11

printer = True
text = True


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

dicts = [imshow_dict(generic_dict, alice_win_percent[alice_lower:, bob_lower:], "Alice's Win Percentage"),
         imshow_dict(generic_dict, alice_draw_percent[alice_lower:, bob_lower:], "Alice's Draw Percentage"),
         imshow_dict(generic_dict, alice_loss_percent[alice_lower:, bob_lower:], "Alice's Loss Percentage"),
         imshow_dict(generic_dict, alice_score_ave[alice_lower:, bob_lower:], "Alice's Score Average"),
         imshow_dict(generic_dict, bob_win_percent[alice_lower:, bob_lower:], "Bob's Win Percentage"),
         imshow_dict(generic_dict, bob_draw_percent[alice_lower:, bob_lower:], "Bob's Draw Percentage"),
         imshow_dict(generic_dict, bob_loss_percent[alice_lower:, bob_lower:], "Bob's Loss Percentage"),
         imshow_dict(generic_dict, bob_score_ave[alice_lower:, bob_lower:], "Bob's Score Average")]

if printer:
    for item in dicts:
        print(item["title"])
        print(item["data"])

print("Time:", time.perf_counter())

imshow_multiplot(dicts, 2, 4, text=text)
