import time
time.clock()
import random

class Player:
    def __init__(self, name, strat_):
        self.name = name
        self.backpack = 0
        self.backpack_leavegem = 0
        self.backpack_leaveart = 0
        self.tent = 0
        self.tent_leavegem = 0
        self.tent_leaveart = 0
        self.artifacts = 0
        self.exploring = True
        self.leaving = False
        self.strat = strat_
        self.log = []
        self.wins = 0
        self.draws = 0

    def leave(self, turn):
        return self.strat(turn, self.backpack)

class Cards:
    def __init__(self, cardlist):

        self.cardlist = cardlist
        self.counts = {}
        for card in self.cardlist:
            self.counts.setdefault(card, 0)
            self.counts[card] += 1

    def add(self, card):
        self.cardlist.append(card)
        self.counts.setdefault(card, 0)
        self.counts[card] += 1

    def shuffle(self):
        random.shuffle(self.cardlist)

    def move_top(self, destination):
        card = self.cardlist.pop()
        self.counts[card] -= 1
        destination.add(card)
        return card

    def move_all(self, destination):
        while len(self.cardlist) != 0:
            card = self.cardlist.pop()
            self.counts[card] -= 1
            destination.add(card)

    def move_allspecific(self, destination, cardname):
        self.counts.setdefault(cardname, 0)
        while self.counts[cardname] != 0:
            self.cardlist.remove(cardname)
            self.counts[cardname] -= 1
            destination.add(cardname)

    def move_specific(self, destination, cardname):
        self.cardlist.remove(cardname)
        self.counts[cardname] -= 1
        destination.add(cardname)

class Simulator:
    def __init__(self):
        pass

    def init_game_cards(self):
        self.deck = Cards(["fire", "fire", "fire", "mummy", "mummy", "mummy", "rocks", "rocks", "rocks", "snake", "snake", "snake", "spiders", "spiders", "spiders", 1, 2, 3, 4, 5, 5, 7, 7, 9, 11, 11, 13, 14, 15, 17])
        self.table = Cards([])
        self.discard = Cards([])
        self.reserve = Cards(["artifact", "artifact", "artifact", "artifact", "artifact"])

    def init_player_tent(self):
        for player in self.players:
            player.tent = 0

    def init_player_exploring(self):
        self.num_exploring = len(self.players)
        for player in self.players:
            player.exploring = True

    def init_round_cards(self):
        if len(self.table.cardlist) != 0:
            self.table.move_all(self.deck)
        self.reserve.move_top(self.deck)
        self.deck.shuffle()
        print("reverse order deck", self.deck.cardlist[::-1])
        #print(self.deck.counts)

    def init_player_leaving(self):
        self.num_leaving = 0
        for player in self.players:
            player.leaving = False

    def check_bust(self):
        hazards = ["fire", "mummy", "rocks", "snake", "spiders"]
        for hazard in hazards:
            self.table.counts.setdefault(hazard, 0)
            if self.table.counts[hazard] == 2:
                return True

    def busted(self):
        print("busted table", self.table.cardlist)
        for player in self.players:
            if player.exploring:
                print("busted", player.name, "backpack:", player.backpack, "tent:", player.tent)
                player.exploring = False
                self.num_exploring -= 1
                player.backpack = 0
        self.table.move_top(self.discard)
        self.table_gem = 0
        print("discard", self.discard.cardlist)

    def distribute_gems(self):
        if isinstance(self.card, int):
            #print("----", self.card, "num exploring", self.num_exploring)
            printer = 0
            for player in self.players:
                if player.exploring:
                    if printer == 0:
                        print(self.card, "backpack {} + {} = {}".format(player.backpack, self.card//self.num_exploring, player.backpack + self.card//self.num_exploring), end=" ")
                    printer += 1
                    print(player.name, end=" ")
                    #print(player.name, "backpack {} + {} = {}".format(player.backpack, self.card//self.num_exploring, player.backpack + self.card//self.num_exploring))
                    player.backpack += self.card//self.num_exploring
                    #print(player.name, player.backpack)
            print("table gem {} + {} = {} turn {}".format(self.table_gem, self.card%self.num_exploring, self.table_gem + self.card%self.num_exploring, self.turn))
            self.table_gem += self.card%self.num_exploring
            #print("table gem", self.table_gem)
        else:
            print(self.card, "turn", self.turn)

    def decide_player(self):
        for player in self.players:
            if player.exploring:
                if player.leave(self.turn):
                    print("table", self.table.cardlist)
                    player.exploring = False
                    self.num_exploring -= 1
                    player.leaving = True
                    self.num_leaving += 1

    def leaving_gems(self):
        if self.num_leaving >= 1:
            #print("table gem", self.table_gem, "num leaving", self.num_leaving)
            for player in self.players:
                if player.leaving:
                    #print(player.name, "tent {} + {}".format(player.tent, self.table_gem//self.num_leaving))
                    player.backpack_leavegem = self.table_gem//self.num_leaving
                    #print(player.name, "tent", player.tent)
            self.table_gem = self.table_gem%self.num_leaving
            #print("new table gem", self.table_gem)

    def leaving_artifacts(self):
        self.table.counts.setdefault("artifact", 0)
        self.discard.counts.setdefault("artifact", 0)
        if self.table.counts["artifact"] >= 1 and self.num_leaving == 1:
            for player in self.players:
                if player.leaving:
                    while self.table.counts["artifact"] != 0:
                        if self.discard.counts["artifact"] < 3:
                            #print("{} takes artifact. Tent {} + 5".format(player.name, player.tent))
                            self.table.move_specific(self.discard, "artifact")
                            player.artifacts += 1
                            player.backpack_leaveart += 5
                            #print("{} tent {}, artifacts {}".format(player.name, player.tent, player.artifacts))
                            print("discard", self.discard.cardlist)

                        else:
                            #print("{} takes artifact. Tent {} + 10".format(player.name, player.tent))
                            self.table.move_specific(self.discard, "artifact")
                            player.artifacts += 1
                            player.backpack_leaveart += 10
                            #print("{} tent {}, artifacts {}".format(player.name, player.tent, player.artifacts))
                            print("discard", self.discard.cardlist)
                    break

    def store_backpack(self):
        for player in self.players:
            if player.leaving:
                print("leaving {} {} + {} + {} = {}".format(player.name, player.backpack, player.backpack_leavegem, player.backpack_leaveart, player.backpack + player.backpack_leavegem + player.backpack_leaveart))
                player.backpack += player.backpack_leavegem + player.backpack_leaveart
                player.backpack_leavegem = 0
                player.backpack_leaveart = 0
                print("leaving {} {} + {} = {}".format(player.name, player.tent, player.backpack, player.tent + player.backpack))
                player.tent += player.backpack
                player.backpack = 0

    def log_scores(self):
        self.max_tent = 0
        self.max_player = []
        print("End Game")
        for player in self.players:
            print(player.name, player.tent)
            player.log.append(player.tent)
            if player.tent > self.max_tent:
                self.max_tent = player.tent
                self.max_player = [player]
            elif player.tent == self.max_tent:
                self.max_player.append(player)
        if len(self.max_player) == 1:
            self.max_player[0].wins += 1
        else:
            for player in self.max_player:
                player.draws += 1
        print("max tent", self.max_tent)
        print("max player", [player.name for player in self.max_player])
        for player in self.players:
            print("{} average {} wins {} draws {}".format(player.name, sum(player.log)/len(player.log), player.wins, player.draws))

    def run_round(self):
        self.turn = 0
        self.table_gem = 0

        self.init_player_exploring()
        self.init_round_cards()
        while self.num_exploring > 0:
            self.turn += 1
            self.init_player_leaving()

            self.card = self.deck.move_top(self.table)

            if self.check_bust():
                self.busted()
            else:
                self.distribute_gems()
                self.decide_player()
                self.leaving_gems()
                self.leaving_artifacts()
                self.store_backpack()

    def sim(self, games, players):
        self.games = games
        self.players = players

        for game in range(1, self.games+1):
            print("Start Game", game)
            self.init_game_cards()
            self.init_player_tent()
            for round in range(1, 6):
                print("Round", round)
                self.run_round()
            self.log_scores()


ethan_wins = []
harald_wins = []
ethan_ave = []
harald_ave = []

def leave_turn1(turn, backpack):
    return turn >= x

def leave_turn2(turn, backpack):
    return turn >= x+4

def leave_backpack(turn, backpack):
    return backpack >= 15

for x in range(6, 7):


    ethan = Player("Ethan", leave_turn1)
    harald = Player("Harald", leave_turn2)

    players = [ethan, harald]

    incan = Simulator()
    incan.sim(2, players)

    ethan_wins.append(ethan.wins)
    harald_wins.append(harald.wins)
    ethan_ave.append(sum(ethan.log)/len(ethan.log))
    harald_ave.append(sum(harald.log)/len(harald.log))

print("ethan wins ", ethan_wins)
print("harald wins", harald_wins)
print("ethan ave ", ethan_ave)
print("harald ave", harald_ave)

print("time", time.clock())
