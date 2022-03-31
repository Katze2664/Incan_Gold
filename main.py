import time
time.perf_counter()
from incan_gold import Player
from incan_gold import Simulator


def leave_turn1(turn, backpack):
    return turn >= 6

def leave_turn2(turn, backpack):
    return turn >= 10

def leave_backpack(turn, backpack):
    return backpack >= 12

ethan = Player("Ethan", leave_turn1)
harald = Player("Harald", leave_turn2)
ian = Player("Ian", leave_backpack)

players = [ethan, harald, ian]

incan = Simulator()
incan.sim(1, players)


print("time", time.perf_counter())