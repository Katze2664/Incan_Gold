import random

# Leave when turns reaches max_turns
def make_turn_strat(max_turns):
    def turn_strat(name, turn, backpack):
        return turn >= max_turns
    return turn_strat

# Leave when backpack reaches (or exceeds) max_backpack
def make_backpack_strat(max_backpack):
    def backpack_strat(name, turn, backpack):
        return backpack >= max_backpack
    return backpack_strat

# Leave with a probability of prob_leave
def make_random_strat(prob_leave):
    def random_strat(name, turn, backpack):
        rand = random.random()
        if rand < prob_leave:
            return True
        else:
            return False
    return random_strat

# Ask user
def interactive_strat(name, turn, backpack):
    user = input(f"{name}, continue exploring? (y/n): ")
    user = user.lower()
    while user not in ["", "y", "yes", "n", "no", "q", "quit", "exit"]:
        print(f"Invalid input.\n"
              f"For yes, type y or yes or press enter.\n"
              f"For no, type n or no.\n"
              f"To quit, q or quit or exit.\n"
              f"It is not case sensitive.")
        user = input(f"{name}, continue exploring? (y/n): ")
        user = user.lower()
    if user in ["n", "no"]:
        return True
    elif user in ["q", "quit", "exit"]:
        exit()
    else:
        return False
