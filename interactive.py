from game_mechanics import Player, Simulator
from strategies import make_turn_strat, make_backpack_strat, make_random_strat, interactive_strat

# Play an interactive game of Incan Gold against a simple bot

# Enter your name here
your_name = "Alice"
human = Player(your_name, interactive_strat)

# Set random seed if desired.
seed = None

# Some pre-made bot strategies. Modify the parameters if desired.
bot_turn_strat = make_turn_strat(7)  # leaves on turn 7
bot_backpack_strat = make_backpack_strat(20)  # leaves when it has 20 or more in the backpack
bot_random_strat = make_random_strat(0.2)  # leaves with a probability of 0.2 each turn

# enter desired bot strategy here
bot = Player("Bot", bot_random_strat)

players = [human, bot]

incan = Simulator(verbosity=5, manual=False, seed=seed)

print("To continue exploring, you can just press enter instead of typing y.")
incan.sim(1, players)
