import time
time.clock()
import random

class Player:
    def __init__(self, name, strat_):
        self.name = name
        self.backpack = 0
        self.tent = 0
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

# deal top card of deck to table
# take hazard card from table and discard it
# take all artifacts on table and give them to a player
# take artifact from reserve to the deck
# return all cards from table to deck during bust

# Phases of the game:
# Set up the deck, the players and the starting scores.
# Each round, shuffle the deck.
# Each turn, deal a card.
# If bust, all exploring players leave and lose their backpack, discard a hazard, start clean-up.
# Elif gem, distribute to exploring player's backpacks, remainder on table.
# Players decide to stay or go.
# If only one player leaves, they take any artifacts with them.
# Repeat until bust or all players gone.
# Clean-up: return table to deck, add artifact to deck.
# Repaat for 5 rounds.
# Determine winner and put score in log.
# Repeat game to get average winner.

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
        print(self.deck.counts)

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
            print("----", self.card, "num exploring", self.num_exploring)
            for player in self.players:
                if player.exploring:
                    print(player.name, "backpack {} + {}".format(player.backpack, self.card//self.num_exploring))
                    player.backpack += self.card//self.num_exploring
                    print(player.name, player.backpack)
            print("table gem {} + {}".format(self.table_gem, self.card%self.num_exploring))
            self.table_gem += self.card%self.num_exploring
            print("table gem", self.table_gem)
        else:
            print("----", self.card)

    def decide_player(self):
        for player in self.players:
            if player.exploring:
                if player.leave(self.turn):
                    player.exploring = False
                    self.num_exploring -= 1
                    player.leaving = True
                    self.num_leaving += 1
                    print("leave", player.name, "backpack:", player.backpack, "tent", player.tent)
                    player.tent += player.backpack
                    player.backpack = 0

    def leaving_gems(self):
        if self.num_leaving >= 1:
            print("table gem", self.table_gem, "num leaving", self.num_leaving)
            for player in self.players:
                if player.leaving:
                    print(player.name, "tent {} + {}".format(player.tent, self.table_gem//self.num_leaving))
                    player.tent += self.table_gem//self.num_leaving
                    print(player.name, "tent", player.tent)
            self.table_gem = self.table_gem%self.num_leaving
            print("new table gem", self.table_gem)

    def leaving_artifacts(self):
        self.table.counts.setdefault("artifact", 0)
        self.discard.counts.setdefault("artifact", 0)
        if self.table.counts["artifact"] >= 1 and self.num_leaving == 1:
            for player in self.players:
                if player.leaving:
                    while self.table.counts["artifact"] != 0:
                        if self.discard.counts["artifact"] < 3:
                            print("{} takes artifact. Tent {} + 5".format(player.name, player.tent))
                            self.table.move_specific(self.discard, "artifact")
                            player.artifacts += 1
                            player.tent += 5
                            print("{} tent {}, artifacts {}".format(player.name, player.tent, player.artifacts))
                            print(self.discard.cardlist)

                        else:
                            print("{} takes artifact. Tent {} + 10".format(player.name, player.tent))
                            self.table.move_specific(self.discard, "artifact")
                            player.artifacts += 1
                            player.tent += 10
                            print("{} tent {}, artifacts {}".format(player.name, player.tent, player.artifacts))
                            print(self.discard.cardlist)
                    break

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

for x in range(1, 20):
    def leave_turn1(turn, backpack):
        return turn >= x

    def leave_turn2(turn, backpack):
        return turn >= x+1

    def leave_backpack(turn, backpack):
        return backpack >= 15

    ethan = Player("Ethan", leave_turn1)
    harald = Player("Harald", leave_turn2)

    players = [ethan, harald]

    incan = Simulator()
    incan.sim(1000, players)

    ethan_wins.append(ethan.wins)
    harald_wins.append(harald.wins)
    ethan_ave.append(sum(ethan.log)/len(ethan.log))
    harald_ave.append(sum(harald.log)/len(harald.log))

print("ethan wins ", ethan_wins)
print("harald wins", harald_wins)
print("ethan ave ", ethan_ave)
print("harald ave", harald_ave)

print("time", time.clock())

"""def sim(games, players):

    def busted(table):
        hazards = ["fire", "mummy", "rocks", "snake", "spiders"]
        for hazard in hazards:
            table.counts.setdefault(hazard, 0)
            if table.counts[hazard] == 2:
                return True

    for game in range(1, games+1):
        deck = Cards(["fire", "fire", "fire", "mummy", "mummy", "mummy", "rocks", "rocks", "rocks", "snake", "snake", "snake", "spiders", "spiders", "spiders", 1, 2, 3, 4, 5, 5, 7, 7, 9, 11, 11, 13, 14, 15, 17])
        table = Cards([])
        discard = Cards([])
        reserve = Cards(["artifact", "artifact", "artifact", "artifact", "artifact"])

        for round in range(1, 6):
            print("\nRound", round)
            turn = 0
            table_gem = 0

            num_exploring = len(players)
            for player in players:
                player.exploring = True

            # Prepares deck from previous round.
            if len(table.cardlist) != 0:
                table.move_all(deck)
            reserve.move_top(deck)
            deck.shuffle()
            print("reverse order deck", deck.cardlist[::-1])
            print(deck.counts)

            while num_exploring > 0:
                turn += 1
                num_leaving = 0
                for player in players:
                    player.leaving = False
                #print("turn", turn)
                card = deck.move_top(table)
                #print(card, "(", turn, ")")

                # Check if busted by hazards. End the exploring players, discard a hazard.
                if busted(table):
                    print("busted table", table.cardlist)
                    #print("num players", num_exploring)
                    for player in players:
                        if player.exploring:
                            print("busted", player.name, "backpack:", player.backpack, "tent:", player.tent)
                            player.exploring = False
                            num_exploring -= 1
                            player.backpack = 0
                    #print("num players", num_exploring)
                    #print("table gems", table_gem)
                    #print("table", table.cardlist)
                    #print("discard", discard.cardlist)
                    table.move_top(discard)
                    table_gem = 0
                    #print("table gems", table_gem)
                    #print("table", table.cardlist)
                    print("discard", discard.cardlist)
                else:
                    # Distribute gems to players who are exploring.
                    if isinstance(card, int):
                        print("card", card, "num exploring", num_exploring)
                        for player in players:
                            if player.exploring:
                                print(player.name, "backpack {} + {}".format(player.backpack, card//num_exploring))
                                player.backpack += card//num_exploring
                                print(player.name, player.backpack)
                        print("table gem {} + {}".format(table_gem, card%num_exploring))
                        table_gem += card%num_exploring
                        print("table gem", table_gem)
                    else:
                        print(card)

                    # Allow exploring players to decide if they keep exploring.
                    for player in players:
                        if player.exploring:
                            if player.leave(turn):
                                player.exploring = False
                                num_exploring -= 1
                                player.leaving = True
                                num_leaving += 1
                                print("leave", player.name, "backpack:", player.backpack, "tent", player.tent)
                                player.tent += player.backpack
                                player.backpack = 0

                    # Distribute table gems to players who are leaving.
                    if num_leaving >= 1:
                        print("table gem", table_gem, "num leaving", num_leaving)
                        for player in players:
                            if player.leaving:
                                print(player.name, "tent {} + {}".format(player.tent, table_gem//num_leaving))
                                player.tent += table_gem//num_leaving
                                print(player.name, "tent", player.tent)
                        table_gem = table_gem%num_leaving
                        print("new table gem", table_gem)

                    # Distribute artifacts if just one player is leaving. 5 points for first 3 artifacts, 10 points for the rest.
                    table.counts.setdefault("artifact", 0)
                    discard.counts.setdefault("artifact", 0)
                    if table.counts["artifact"] >= 1 and num_leaving == 1:
                        for player in players:
                            if player.leaving:
                                while table.counts["artifact"] != 0:
                                    if discard.counts["artifact"] < 3:
                                        print("{} takes artifact. Tent {} + 5".format(player.name, player.tent))
                                        table.move_specific(discard, "artifact")
                                        player.artifacts += 1
                                        player.tent += 5
                                        print("{} tent {}, artifacts {}".format(player.name, player.tent, player.artifacts))
                                        print(discard.cardlist)

                                    else:
                                        print("{} takes artifact. Tent {} + 10".format(player.name, player.tent))
                                        table.move_specific(discard, "artifact")
                                        player.artifacts += 1
                                        player.tent += 10
                                        print("{} tent {}, artifacts {}".format(player.name, player.tent, player.artifacts))
                                        print(discard.cardlist)
                                break"""







"""num_explorers = len(player_list)
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

    print(harald.backpack, "harald backpack6")"""








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

"""class Game:

    def __init__(self, players):
        self.deck = Cards(["fire", "fire", "fire", "mummy", "mummy", "mummy", "rocks", "rocks", "rocks", "snake", "snake", "snake", "spiders", "spiders", "spiders", 1, 2, 3, 4, 5, 5, 7, 7, 9, 11, 11, 13, 14, 15, 17])
        self.table = Cards([])
        self.discard = Cards([])
        self.reserve = Cards(["artifact", "artifact", "artifact", "artifact", "artifact"])
        self.round = 0
        self.MAX_ROUNDS = 5
        self.num_players = len(players)
        self.players = players

    def initialise_players(self):
        for player in self.players:
            player.explore = True

    def play_round(self):
        self.round += 1
        if self.round > self.MAX_ROUNDS:
            #dont play any more, finsih up the game
        print("\nRound {}".format(self.round))
        self.turn = 0
        self.table_gem = 0
        self.initialise_players()"""

