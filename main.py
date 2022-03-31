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

leave_turn_4 = make_turn_strat(4)
leave_turn_6 = make_turn_strat(6)
leave_turn_10 = make_turn_strat(10)

ethan = Player("Ethan", leave_turn_6)
harald = Player("Harald", leave_turn_10)
ian = Player("Ian", leave_turn_4)

players = [ethan, harald, ian]

incan = Simulator(verbose=1, manual=False, seed=1)
incan.sim(5, players)
incan.sim(5, players)
incan.sim(5, players)

print("time", time.perf_counter())
