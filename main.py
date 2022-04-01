from incan_gold import Player, Simulator
from strategies import make_turn_strat, make_backpack_strat, make_random_strat, interactive_strat

# alice leaves on turn 7
turn_strat = make_turn_strat(7)
alice = Player("Alice", turn_strat)

# bob leaves when he has 20 or more in his backpack
backpack_strat = make_backpack_strat(20)
bob = Player("Bob", backpack_strat)

# charlie leaves with a probability of 0.2 each turn
random_strat = make_random_strat(0.2)
charlie = Player("Charlie", random_strat)

players = [alice, bob, charlie]

# verbose=1 will show the result after all games are complete.
incan = Simulator(verbose=1, manual=False)

# plays 100 games
games = 100
incan.sim(games, players)
