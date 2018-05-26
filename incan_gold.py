import random

class Player:
    def __init__(self, name_, strat_):
        self.name = name_
        self.backpack = 0
        self.tent = 0
        self.art_tent = 0
        self.explore = True
        self.leaving = False
        self.strat = strat_

    def playon(self, turn):
        return self.strat(turn, self.backpack)

class Cards:
    def __init__(self, cardlist):

        self.cardlist = cardlist
        self.counts = {}
        for card in self.cardlist:
            self.counts.setdefault(card, 0)
            self.counts[card] += 1
        print(self.counts)

    def add(self, card):
        self.cardlist.append(card)
        self.counts.setdefault(card, 0)
        self.counts[card] += 1

    def shuffle(self):
        random.shuffle(self.cardlist)
        print(self.cardlist)

    def move_top(self, destination):
        card = self.cardlist.pop(0)
        self.counts[card] -= 1
        destination.add(card)
        print(card)
        print(self.counts)
        print(destination.counts)

    def move_all(self, destination, cardtype="all"):
        for i in range(len(self.cardlist)-1, -1, -1):
            if cardtype == "all" or self.cardlist[i] == cardtype:
                card = self.cardlist.pop(i)
                self.counts[card] -= 1
                destination.add(card)


    # deal top card of deck to table
    # take hazard card from table and discard it
    # take all artifacts on table and give them to a player
    # take artifact from reserve to the deck
    # return all cards from table to deck during bust


    def table2deck(self, card):
        self.table_list.append(card)
        self.deck_dict[card] += -1
        self.table_dict[card] += 1
        self.gem_table2deck(card)

    def table2discard(self, card):
        self.table_list.remove(card)
        self.discard_list.append(card)
        self.table_dict[card] += -1
        self.discard_dict[card] += 1

    def reserve2deck(self, card):
        self.table_list.remove(card)
        self.discard_list.append(card)
        self.table_dict[card] += -1
        self.discard_dict[card] += 1

deck = Cards(["artifact", "fire", "fire", "fire", "mummy", "mummy", "mummy", "rocks", "rocks", "rocks", "snake", "snake", "snake", "spiders", "spiders", "spiders", 1, 2, 3, 4, 5, 5, 7, 7, 9, 11, 11, 13, 14, 15, 17])
table = Cards([])
discard = Cards([])
reserve = Cards(["artifact", "artifact", "artifact", "artifact"])

deck.shuffle()
deck.deal(table)

"""blah.shuffle()

for i in range(3):
    blah.deal()
    print(blah.deck_list)
    print(blah.table_list)
    print(blah.deck_dict)
    print(blah.table_dict)
    print(blah.gem_value_deck)
    print(blah.gem_value_table)"""



"""if card == "artifact":
    self.artifact_deck += -1
    self.artifact_table += 1
elif card == "fire":
    self.fire_deck += -1
    self.fire_table += 1
elif card == "mummy":
    self.mummy_deck += -1
    self.mummy_table += 1
elif card == "rocks":
    self.rocks_deck += -1
    self.rocks_table += 1
elif card == "snake":
    self.snake_deck += -1
    self.snake_table += 1
elif card == "spiders":
    self.spiders_deck += -1
    self.spiders_table += 1
else:
    self.gem_num_deck += -1
    self.gem_num_table += 1
    self.gem_value_deck += -card
    self.gem_value_table += card
    self.gem_deck_list.remove(card)

print("card", card)
print("deck", self.deck_list)
print("table", self.table_list)
print("discard", self.discard_list)
print("reserve", self.reserve_list)
print(\
"art",\
self.artifact_deck,\
self.artifact_table,\
self.artifact_discard,\
self.artifact_reserve,\
"fire",\
self.fire_deck,\
self.fire_table,\
self.fire_discard,\
"mummy",\
self.mummy_deck,\
self.mummy_table,\
self.mummy_discard,\
"rocks",\
self.rocks_deck,\
self.rocks_table,\
self.rocks_discard,\
"snake",\
self.snake_deck,\
self.snake_table,\
self.snake_discard,\
"spiders",\
self.spiders_deck,\
self.spiders_table,\
self.spiders_discard,\
"gems",\
self.gem_num_deck,\
self.gem_num_table,\
self.gem_value_deck,\
self.gem_value_table)

def check_bust(self):
busted = False
if self.fire_table == 2:
    busted = True
    self.table_list.remove("fire")
    self.discard_list.append("fire")
    self.fire_table += -1
    self.fire_discard += 1
elif self.mummy_table == 2:
    busted = True
    self.table_list.remove("mummy")
    self.discard_list.append("mummy")
    self.mummy_table += -1
    self.mummy_discard += 1
elif self.rocks_table == 2:
    busted = True
    self.table_list.remove("rocks")
    self.discard_list.append("rocks")
    self.rocks_table += -1
    self.rocks_discard += 1
elif self.snake_table == 2:
    busted = True
    self.table_list.remove("snake")
    self.discard_list.append("snake")
    self.snake_table += -1
    self.snake_discard += 1
elif self.spiders_table == 2:
    busted = True
    self.table_list.remove("spiders")
    self.discard_list.append("spiders")
    self.spiders_table += -1
    self.spiders_discard += 1
return busted"""







"""def strat_turn(turn, backpack):
    return turn <= 3
# strat_turn = lambda turn, backpack: turn <= 3

def strat_backpack(turn, backpack):
    return backpack <= 5

ethan = Player("Ethan", strat_turn)
harald = Player("Harald", strat_backpack)
player_list = [ethan, harald]

deck = [1, 2, 3, 4, 5, 5, 7, 7, 9, 11, 11, 13, 14, 15, 17, "art", "art", "art", "art", "art", "fire", "fire", "fire", "snake", "snake", "snake", "mummy", "mummy", "mummy", "rocks", "rocks", "rocks", "spiders", "spiders", "spiders"]



def game(player_list):
    num_explorers = len(player_list)
    art = 0
    art_taken = 0
    gems = 0
    fire = 0
    fire_discard = 0
    snake = 0
    snake_discard = 0
    mummy = 0
    mummy_discard = 0
    rocks = 0
    rocks_discard = 0
    spiders = 0
    spiders_discard = 0
    discarded = []
    turn = 0
    busted = False

    while num_explorers >= 1:
        turn += 1
        print("turn", turn)
        card = random.choice(deck)
        deck.remove(card)
        print("card", card)
        print("deck", deck)

        if card == "art":
            art += 1
        elif card == "fire":
            fire += 1
            if fire == 2:
                busted = True
                deck.remove("fire")
                discarded.append("fire")
        elif card == "snake":
            snake += 1
            if snake == 2:
                busted = True
                deck.remove("snake")
                discarded.append("snake")
        elif card == "mummy":
            mummy += 1
            if mummy == 2:
                busted = True
                deck.remove("mummy")
                discarded.append("mummy")
        elif card == "rocks":
            rocks += 1
            if rocks == 2:
                busted = True
                deck.remove("rocks")
                discarded.append("rocks")
        elif card == "spiders":
            spiders += 1
            if spiders == 2:
                busted = True
                deck.remove("spiders")
                discarded.append("spiders")
        else:
            if busted == False:
                for player in player_list:
                    if player.explore == True:
                        player.backpack += card//num_explorers
                        print(player.name, "backpack", player.backpack)
                gems += card%num_explorers
        print("art {}, fire {}, snake {}, mummy {}, rocks {}, spiders {}, gems {}".format(art, fire, snake, mummy, rocks, spiders, gems))
        print("deck", deck)
        print("discarded", discarded)

        print(harald.backpack, "harald backpack")

        if busted == True:
            for player in player_list:
                if player.explore == True:
                    player.backpack = 0
                    player.explore = False
                    num_explorers += -1

            gems = 0
            art = 0

        print(harald.backpack, "harald backpack2")

        num_leaving = 0
        
        for player in player_list:
            if player.explore == True:
                if player.playon(turn) == False:
                    player.explore = False
                    player.leaving = True
                    num_explorers += -1
                    num_leaving += 1
                    player.tent += player.backpack
                    player.backpack = 0

        print(harald.backpack, "harald backpack3")

        # distributing artifacts if a player is leaving alone on this turn
        if num_leaving == 1:
            for player in player_list:
                if player.leaving == True:
                    while art != 0:
                        player.art_tent += art
                        if art_taken <= 3:
                            player.tent += 5
                            art_taken += 1
                            discarded.append("art")
                            art += -1
                        else:
                            player.tent += 10
                            art_taken += 1
                            discarded.append("art")
                            art += -1

        print(harald.backpack, "harald backpack4")

        #distributing gems to players leaving on this turn
        if num_leaving > 0:
            for player in player_list:
                if player.leaving == True:
                    player.tent += gems//num_leaving
                    player.leaving = False
            gems = gems%num_leaving
            num_leaving = 0

        print(harald.backpack, "harald backpack5")

        for player in player_list:
            if player.playon(turn) == True:
                print(player.name, "playon", player.backpack)
            else:
                print(player.name, "leave", player.backpack)

        print(harald.backpack, "harald backpack6")




                


game(player_list)

"""
