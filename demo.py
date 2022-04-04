import time
time.perf_counter()
from game_mechanics import Player, Simulator
from strategies import make_turn_strat, make_backpack_strat, make_random_strat, interactive_strat

# Demonstration of 3 bots with different strategies playing Incan Gold

# Set demo = 1 to play 100 games in quick succession and see summary statistics once all games are complete.
# Set demo = 2 to play 1 game turn-wise with detailed information about each turn.
demo = 1

# Set random seed if desired.
seed = None

# Modify strategies below if desired.
# Alice leaves on turn 7
turn_strat = make_turn_strat(7)
alice = Player("Alice", turn_strat)

# Bob leaves when he has 20 or more in his backpack
backpack_strat = make_backpack_strat(20)
bob = Player("Bob", backpack_strat)

# Charlie leaves with a probability of 0.2 each turn
random_strat = make_random_strat(0.2)
charlie = Player("Charlie", random_strat)

players = [alice, bob, charlie]

if demo == 1:
    # verbosity=1 will show the result after all games are complete.
    # manual=False will play the game automatically without asking for user input at the start of each turn.
    incan = Simulator(verbosity=1, manual=False, seed=seed)
    games = 100
    incan.sim(games, players)
    print("\nProgram run time (seconds):", time.perf_counter())

if demo == 2:
    # verbosity=5 will show the detail of each turn being played.
    # manual=True will ask the user to press enter at the start of each turn.
    incan = Simulator(verbosity=5, manual=True, seed=seed)
    games = 1
    incan.sim(games, players)
