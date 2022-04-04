from game_mechanics import Simulator

# This code is incomplete and under development.

# It is for estimating probabilities that are relevant for more complicated decision strategies, such as:
# the probability that the next card will cause a bust,
# the value of gems remaining when split between the number of players currently exploring,
# the probability that n players will leave this turn assuming the probability is known for each player individually
# the expected value of the next card assuming a probability distribution over n players leaving this turn,
# the expected value of an artifact assuming a probability distribution over n players leaving this turn,.


class ProbabilitySimulator(Simulator):
    def __init__(self):
        pass

    def chance_bust(self):
        bust_cards = 0
        hazards = ["fire", "mummy", "rocks", "snake", "spiders"]
        for hazard in hazards:
            self.table.counts.setdefault(hazard, 0)
            if self.table.counts[hazard] == 1:
                self.deck.counts.setdefault(hazard, 0)
                bust_cards += self.deck.counts[hazard]
        return bust_cards, len(self.deck.card_list), bust_cards / len(self.deck.card_list)

    def next_card_value(self):
        gem_total = 0
        gem_ind = 0
        gems = [1, 2, 3, 4, 5, 7, 9, 11, 13, 14, 15, 17]
        for gem in gems:
            self.deck.counts.setdefault(gem, 0)
            gem_total += self.deck.counts[gem]*gem
            gem_ind += self.deck.counts[gem]*(gem // self.num_exploring)
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
        result = 0
        for i in range(len(num_leave)):
            result += num_leave[i]*(self.table_gem // (i+1))
        return result

    def expected_artifact(self, list_prob_leave):
        num_leave = self.prob_num_leave(list_prob_leave)
        return num_leave[0]*self.table_art

    def run_round(self):
        self.turn = 0
        self.table_gem = 0
        self.table_art = 0

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
                print(self.expected_artifact([0.5, 0.5]))
                self.decide_player()
                self.leaving_gems()
                self.leaving_artifacts()
                self.store_backpack()

    # Old version of prob_num_leave()
    # def prob_num_others_leave(self):
    #     result = [0, 0, 0, 0]
    #     prob_leave = [0.1, 0.3, 0.4]
    #     prob_stay = []
    #     for i in prob_leave:
    #         prob_stay.append(1-i)
    #
    #     for i in range(2):
    #         if i == 0:
    #             prob_i = prob_stay[0]
    #         else:
    #             prob_i = prob_leave[0]
    #
    #         for j in range(2):
    #             if j == 0:
    #                 prob_j = prob_stay[1]
    #             else:
    #                 prob_j = prob_leave[1]
    #
    #             for k in range(2):
    #                 if k == 0:
    #                     prob_k = prob_stay[2]
    #                 else:
    #                     prob_k = prob_leave[2]
    #
    #                 num_leave = i+j+k
    #                 result[num_leave] += prob_i*prob_j*prob_k
    #     return result