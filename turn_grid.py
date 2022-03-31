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

ethan_wins = []
harald_wins = []
ethan_ave = []
harald_ave = []

x_max = 20
y_max = 20


for y in range(1, y_max+1):
    leave_turn_y = make_turn_strat(y)

    ethan_wins.append([])
    harald_wins.append([])
    ethan_ave.append([])
    harald_ave.append([])

    for x in range(1, x_max+1):
        leave_turn_x = make_turn_strat(x)

        ethan = Player("Ethan", leave_turn_y)
        harald = Player("Harald", leave_turn_x)

        players = [ethan, harald]

        incan = Simulator()
        incan.sim(10, players)

        ethan_wins[y-1].append(ethan.wins)
        harald_wins[y-1].append(harald.wins)
        ethan_ave[y-1].append(sum(ethan.log)/len(ethan.log))
        harald_ave[y-1].append(sum(harald.log)/len(harald.log))

print("\nethan wins")
for y in range(1, y_max+1):
    print(ethan_wins[y-1])

print("\nharald wins")
for y in range(1, y_max+1):
    print(harald_wins[y-1])

print("\nethan ave")
for y in range(1, y_max+1):
    print(ethan_ave[y-1])

print("\nharald ave")
for y in range(1, y_max+1):
    print(harald_ave[y-1])
