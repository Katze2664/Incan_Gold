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
        #p-rint(self.deck.counts)

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
            #p-rint("----", self.card, "num exploring", self.num_exploring)
            counter = 0
            for player in self.players:
                if player.exploring:
                    if counter == 0:
                        print(self.card, "backpack {} + {} = {}".format(player.backpack, self.card//self.num_exploring, player.backpack + self.card//self.num_exploring), end=" ")
                        pass
                    counter += 1
                    print(player.name, end=" ")
                    #p-rint(player.name, "backpack {} + {} = {}".format(player.backpack, self.card//self.num_exploring, player.backpack + self.card//self.num_exploring))
                    player.backpack += self.card//self.num_exploring
                    #p-rint(player.name, player.backpack)
            print("table gem {} + {} = {} turn {}".format(self.table_gem, self.card%self.num_exploring, self.table_gem + self.card%self.num_exploring, self.turn))
            self.table_gem += self.card%self.num_exploring
            #p-rint("table gem", self.table_gem)
        else:
            print(self.card, "turn", self.turn)
            pass

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
            #p-rint("table gem", self.table_gem, "num leaving", self.num_leaving)
            for player in self.players:
                if player.leaving:
                    #p-rint(player.name, "tent {} + {}".format(player.tent, self.table_gem//self.num_leaving))
                    player.backpack_leavegem = self.table_gem//self.num_leaving
                    #p-rint(player.name, "tent", player.tent)
            self.table_gem = self.table_gem%self.num_leaving
            #p-rint("new table gem", self.table_gem)

    def leaving_artifacts(self):
        self.table.counts.setdefault("artifact", 0)
        self.discard.counts.setdefault("artifact", 0)
        if self.table.counts["artifact"] >= 1 and self.num_leaving == 1:
            for player in self.players:
                if player.leaving:
                    while self.table.counts["artifact"] != 0:
                        if self.discard.counts["artifact"] < 3:
                            #p-rint("{} takes artifact. Tent {} + 5".format(player.name, player.tent))
                            self.table.move_specific(self.discard, "artifact")
                            player.artifacts += 1
                            player.backpack_leaveart += 5
                            #p-rint("{} tent {}, artifacts {}".format(player.name, player.tent, player.artifacts))
                            print("discard", self.discard.cardlist)

                        else:
                            #p-rint("{} takes artifact. Tent {} + 10".format(player.name, player.tent))
                            self.table.move_specific(self.discard, "artifact")
                            player.artifacts += 1
                            player.backpack_leaveart += 10
                            #p-rint("{} tent {}, artifacts {}".format(player.name, player.tent, player.artifacts))
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
            pass

    def chance_bust(self):
        bust_cards = 0
        hazards = ["fire", "mummy", "rocks", "snake", "spiders"]
        for hazard in hazards:
            self.table.counts.setdefault(hazard, 0)
            if self.table.counts[hazard] == 1:
                self.deck.counts.setdefault(hazard, 0)
                bust_cards += self.deck.counts[hazard]
        return bust_cards, len(self.deck.cardlist), bust_cards/len(self.deck.cardlist)

    def next_card_value(self):
        gem_total = 0
        gem_ind = 0
        gems = [1, 2, 3, 4, 5, 7, 9, 11, 13, 14, 15, 17]
        for gem in gems:
            self.deck.counts.setdefault(gem, 0)
            gem_total += self.deck.counts[gem]*gem
            gem_ind += self.deck.counts[gem]*(gem//self.num_exploring)
        return gem_total, gem_ind

    def prob_num_leave(self, list_prob_leave):
        result = [0]
        list_prob_stay = []
        for p in list_prob_leave:
            result.append(0)
            list_prob_stay.append(1-p)

        for i in range(2**len(list_prob_leave)):
            num_leave = 0
            prob_leave = 1
            for person in range(len(list_prob_leave)):
                if i & 2**person:
                    num_leave += 1
                    prob_leave *= list_prob_leave[person]
                else:
                    prob_leave *= list_prob_stay[person]
            result[num_leave] += prob_leave
        return result

    def expected_table_gem(self, list_prob_leave):
        num_leave = self.prob_num_leave(list_prob_leave)
        table_gem_ind = []
        exp_table_gem = []
        result = 0
        result2 = 0
        for i in range(len(num_leave)):
            table_gem_ind.append(self.table_gem//(i+1))
            exp_table_gem.append(num_leave[i]*table_gem_ind[i])
            result += exp_table_gem[i]
            result2 += num_leave[i]*(self.table_gem//(i+1))
        return table_gem_ind, exp_table_gem, result, result2
            
    

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
                print(self.chance_bust())
                print(self.next_card_value())
                print(self.prob_num_leave([0.5, 0.5]))
                print(self.expected_table_gem([0.5, 0.5]))
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

"""def prob_num_others_leave(self):
        result = [0, 0, 0, 0]
        prob_leave = [0.1, 0.3, 0.4]
        prob_stay = []
        for i in prob_leave:
            prob_stay.append(1-i)

        for i in range(2):
            if i == 0:
                prob_i = prob_stay[0]
            else:
                prob_i = prob_leave[0]

            for j in range(2):
                if j == 0:
                    prob_j = prob_stay[1]
                else:
                    prob_j = prob_leave[1]

                for k in range(2):
                    if k == 0:
                        prob_k = prob_stay[2]
                    else:
                        prob_k = prob_leave[2]

                    num_leave = i+j+k
                    result[num_leave] += prob_i*prob_j*prob_k
        return result"""

"""ethan_wins = []
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
    print(harald_ave[y-1])"""

print("time", time.clock())
