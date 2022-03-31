from incan_gold import Player, Simulator
from strategies import make_turn_strat, make_backpack_strat, make_random_strat, interactive_strat

# Interactive game against a simple bot

bot_turn_strat = make_turn_strat(7)
bot_backpack_strat = make_backpack_strat(20)
bot_random_strat = make_random_strat(0.2)

your_name = "Alice"

human = Player(your_name, interactive_strat)

# enter desired bot strategy here
bot = Player("Bot", bot_turn_strat)

players = [human, bot]

incan = Simulator(verbose=5, manual=False)
incan.sim(1, players)