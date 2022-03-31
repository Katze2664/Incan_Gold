from incan_gold import Player
from incan_gold import Simulator

def leave_turn1(turn, backpack):
    return turn >= 6

def leave_turn2(turn, backpack):
    return turn >= 10

ethan_wins = []
harald_wins = []
ethan_ave = []
harald_ave = []

x_max = 20
y_max = 20

for y in range(1, y_max+1):
    ethan_wins.append([])
    harald_wins.append([])
    ethan_ave.append([])
    harald_ave.append([])

    for x in range(1, x_max+1):
        ethan = Player("Ethan", leave_turn1)
        harald = Player("Harald", leave_turn2)

        players = [ethan, harald]

        if x == 9 and y == 1:
            print("x == 9, y == 1")
            pass

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
