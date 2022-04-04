import random

class Player:
    def __init__(self, name, strat):
        self.name = name
        self.backpack = 0
        self.backpack_leave_gem = 0
        self.backpack_leave_art = 0
        self.tent = 0
        self.tent_leave_gem = 0
        self.tent_leave_art = 0
        self.artifacts = 0
        self.exploring = True
        self.leaving = False
        self.strat = strat
        self.log = []
        self.wins = 0
        self.draws = 0
        self.losses = 0

    def leave(self, turn):
        return self.strat(self.name, turn, self.backpack)

class Cards:
    def __init__(self, card_list):

        self.card_list = card_list
        self.counts = {}
        for card in self.card_list:
            self.counts.setdefault(card, 0)
            self.counts[card] += 1

    def add(self, card):
        self.card_list.append(card)
        self.counts.setdefault(card, 0)
        self.counts[card] += 1

    def shuffle(self):
        random.shuffle(self.card_list)

    def move_top(self, destination):
        card = self.card_list.pop()
        self.counts[card] -= 1
        destination.add(card)
        return card

    def move_all(self, destination):
        while len(self.card_list) != 0:
            card = self.card_list.pop()
            self.counts[card] -= 1
            destination.add(card)

    def move_all_specific(self, destination, card_name):
        self.counts.setdefault(card_name, 0)
        while self.counts[card_name] != 0:
            self.card_list.remove(card_name)
            self.counts[card_name] -= 1
            destination.add(card_name)

    def move_specific(self, destination, card_name):
        self.card_list.remove(card_name)
        self.counts[card_name] -= 1
        destination.add(card_name)

class Simulator:
    def __init__(self, verbosity=0, manual=False, seed=None):
        self.verbosity = verbosity
        self.manual = manual
        random.seed(seed)

    def init_game_cards(self):
        self.deck = Cards(["fire", "fire", "fire",
                           "mummy", "mummy", "mummy",
                           "rocks", "rocks", "rocks",
                           "snake", "snake", "snake",
                           "spiders", "spiders", "spiders",
                           1, 2, 3, 4, 5, 5, 7, 7, 9, 11, 11, 13, 14, 15, 17])
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
            player.backpack_leave_gem = 0
            player.backpack_leave_art = 0
            player.backpack = 0

    def init_round_cards(self):
        if len(self.table.card_list) != 0:
            self.table.move_all(self.deck)
        self.reserve.move_top(self.deck)
        self.deck.shuffle()

    def init_player_leaving(self):
        self.num_leaving = 0
        for player in self.players:
            player.leaving = False

    def check_bust(self):
        hazards = ["fire", "mummy", "rocks", "snake", "spiders"]
        for hazard in hazards:
            self.table.counts.setdefault(hazard, 0)
            if self.table.counts[hazard] == 2:
                if self.verbosity >= 4:
                    print("Busted!")
                return True

    def busted(self):
        for player in self.players:
            if player.exploring:
                player.exploring = False
                self.num_exploring -= 1
                player.backpack = 0
        self.table.move_top(self.discard)
        self.table_gem = 0

    def distribute_gems(self):
        if self.card == "artifact":
            self.discard.counts.setdefault("artifact", 0)
            if self.table.counts["artifact"] + self.discard.counts["artifact"] <= 3:
                self.table_art += 5
            else:
                self.table_art += 10

        if isinstance(self.card, int):
            for player in self.players:
                if player.exploring:
                    if self.verbosity >= 5:
                        print(f"{player.name}'s backpack: {player.backpack} + {self.card // self.num_exploring} = {player.backpack + self.card // self.num_exploring}")
                    player.backpack += self.card // self.num_exploring
                else:
                    if self.verbosity >= 5:
                        print(f"{player.name}'s backpack: {player.backpack}")
            self.table_gem += self.card % self.num_exploring

        else:
            if self.verbosity >= 5:
                for player in self.players:
                    print(f"{player.name}'s backpack: {player.backpack}")

        if self.verbosity >= 5:
            print(f"Spare gems: {self.table_gem}")
            print(f"Spare artifacts: {self.table_art}")

    def decide_player(self):
        if self.verbosity >= 5:
            leaving_list = []

        for player in self.players:
            if player.exploring:
                if player.leave(self.turn):
                    if self.verbosity >= 5:
                        leaving_list.append(player.name)
                    player.exploring = False
                    self.num_exploring -= 1
                    player.leaving = True
                    self.num_leaving += 1

        if self.verbosity >= 5:
            if len(leaving_list) == 0:
                print("Everyone keeps exploring")
            else:
                print(f"Leaving: {', '.join(leaving_list)}")

    def leaving_gems(self):
        if self.num_leaving >= 1:
            for player in self.players:
                if player.leaving:
                    player.backpack_leave_gem = self.table_gem // self.num_leaving
            self.table_gem = self.table_gem % self.num_leaving

    def leaving_artifacts(self):
        self.table.counts.setdefault("artifact", 0)
        self.discard.counts.setdefault("artifact", 0)
        if self.table.counts["artifact"] >= 1 and self.num_leaving == 1:
            for player in self.players:
                if player.leaving:
                    while self.table.counts["artifact"] != 0:
                        if self.discard.counts["artifact"] < 3:
                            self.table.move_specific(self.discard, "artifact")
                            player.artifacts += 1
                            player.backpack_leave_art += 5
                            self.table_art -= 5

                        else:
                            self.table.move_specific(self.discard, "artifact")
                            player.artifacts += 1
                            player.backpack_leave_art += 10
                            self.table_art -= 10
                    break

    def store_backpack(self):
        someone_leaving = False
        for player in self.players:
            if player.leaving:
                someone_leaving = True
                break

        for player in self.players:
            if player.leaving:
                if self.verbosity >= 5:
                    print(f"{player.name}'s backpack: {player.backpack} + {player.backpack_leave_gem} + {player.backpack_leave_art} = {player.backpack + player.backpack_leave_gem + player.backpack_leave_art}")
                player.backpack += player.backpack_leave_gem + player.backpack_leave_art

            else:
                if self.verbosity >= 5 and someone_leaving:
                    print(f"{player.name}'s backpack: {player.backpack}")

    def log_scores(self):
        self.max_tent = 0
        self.max_player = []
        for player in self.players:
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

        for player in self.players:
            if player not in self.max_player:
                player.losses += 1

        if self.verbosity >= 2:
            print(f"\nWinner(s): {[player.name for player in self.max_player]}")
            for player in self.players:
                print(f"{player.name}'s score = {player.tent}")

    def run_round(self):
        self.turn = 0
        self.table_gem = 0
        self.table_art = 0

        self.init_player_exploring()
        self.init_round_cards()
        while self.num_exploring > 0:
            self.turn += 1

            if self.verbosity >= 4:
                if self.manual:
                    input(f"\nGame {self.game}, Round {self.round}, Turn {self.turn} (press enter): ")
                else:
                    print(f"\nGame {self.game}, Round {self.round}, Turn {self.turn}")

            self.init_player_leaving()

            self.card = self.deck.move_top(self.table)

            if self.verbosity >= 4:
                exploring_list = []
                for player in self.players:
                    if player.exploring:
                        exploring_list.append(player.name)
                print(f"Exploring: {', '.join(exploring_list)}")
                print(f"New card: {self.card}")
                print(f"Table: {self.table.card_list}")

            if self.check_bust():
                self.busted()
            else:
                self.distribute_gems()
                self.decide_player()
                self.leaving_gems()
                self.leaving_artifacts()
                self.store_backpack()

        for player in self.players:
            if self.verbosity >= 3:
                print(f"{player.name}'s tent: {player.tent} + {player.backpack} = {player.tent + player.backpack}")
            player.tent += player.backpack

    def sim(self, games, players):
        self.games = games
        self.players = players
        for player in self.players:
            player.log = []
            player.wins = 0
            player.draws = 0
            player.losses = 0

        for game in range(1, self.games+1):
            self.game = game
            if self.verbosity == 2:
                if self.manual:
                    input(f"\nGame {self.game} (press enter): ")
                else:
                    print(f"\nGame {self.game}")

            self.init_game_cards()
            self.init_player_tent()
            for round_number in range(1, 6):
                self.round = round_number
                if self.verbosity == 3:
                    if self.manual:
                        input(f"\nGame {self.game}, Round {self.round} (press enter): ")
                    else:
                        print(f"\nGame {self.game}, Round {self.round}")

                self.run_round()

            self.log_scores()

        if self.verbosity >= 1:
            print(f"\nTotal games: {self.games}")
            for player in self.players:
                n = len(player.log)
                print(f"\n{player.name}\n"
                      f"Wins: {player.wins} = {round(100 * player.wins / n, 1)}%\n"
                      f"Draws: {player.draws} = {round(100 * player.draws / n, 1)}%\n"
                      f"Losses: {player.losses} = {round(100 * player.losses / n, 1)}%\n"
                      f"Average score: {round(sum(player.log) / n, 1)}")
