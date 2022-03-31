import time
time.perf_counter()
from incan_gold import Player
from incan_gold import Simulator


def make_turn_strat(max_turns):
    def turn_strat(turn, backpack):
        return turn >= max_turns
    return turn_strat

def make_backpack_strat(max_backpack):
    def backpack_strat(turn, backpack):
        return backpack >= max_backpack
    return backpack_strat

leave_turn_6 = make_turn_strat(6)
leave_turn_10 = make_turn_strat(10)

ethan = Player("Ethan", leave_turn_6)
harald = Player("Harald", leave_turn_10)

players = [ethan, harald]

incan = Simulator(verbose=4, manual=False)
incan.sim(1, players)


print("time", time.perf_counter())
