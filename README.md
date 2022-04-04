# Incan Gold

Simulates the board game Incan Gold to test different strategies.

## Description

### Simulation

This program simulates the board game Incan Gold. Due to the random nature of
the game, cards are encountered in a different order every time you play.
This simulation allows different strategies to be automated and tested over 
a large number of games so that statistics can be collected to determine the 
effectiveness of each strategy on average. Each player's score is affected not 
only by the decisions they make, but also by the decisions made by other players.
Hence, this simulation allows different strategies to be played against each other
to determine how they fair in competition. The simulation also allows for user
input so that users can play against bots.

### Original board game

Incan Gold is a push-your-luck board game. Players explore a temple,
collecting treasures and encountering hazards. The deeper into the
temple players go, the more riches they can find. However, if they go
too far and encounter too many hazards they will be scared out of the
temple and lose everything they have collected. The challenge is to
explore long enough to become rich, but leave the temple early enough
that you can keep what you have collected.

### Rules

The game contains 3 types of cards: gems, hazards, and artifacts.  
* The gem cards vary in how many gems they contain. The number of gems on each card is:
1, 2, 3, 4, 5, 5, 7, 7, 9, 11, 11, 13, 14, 15, 17.
* There are 5 types of hazard card: fire, mummy, rocks, snake, spiders. 
  There are 3 copies of each type of hazard.  
* There are 5 artifact cards (which are functionally identical).

The game is composed of 5 rounds. The player with the most treasure at
the end of 5 rounds is the winner.

At the start of the game, the deck is created by shuffling together all the gems,
all the hazards and 1 of the artifacts. The remaining 4 artifacts are put in the reserve pile.

Each round is composed of a series of turns. Each turn proceeds as follows:
1. The top card of the deck is flipped over and placed on the table.
   * If it is a gems card, the gems are distributed evenly into the backpacks of all players
     who are currently exploring, with any remainder (spare gems) staying on the table.
   * If it is a hazard card, nothing happens, unless it is the second copy of the same type of
     hazard, in which case everyone who is currently exploring goes bust and loses everything in
     their backpack and the round ends. The card which caused the bust is placed in the discard pile.
   * If it is an artifact, it remains on the table.
2. Each player who is still exploring decides whether to continue exploring or leave, and the decisions
   are revealed simultaneously.
   * The spare gems are distributed evenly into the backpacks of all players who leave, 
     with any remainder staying on the table.
   * If exactly 1 person leaves, they take all the artifacts on the table and put them in their backpack. 
     The first 3 artifacts to be claimed in the game are worth 5 gems each, and after that they are worth 10 gems each.
   * All players who leave transfer all the gems in their backpack to their tent where they are safe 
     for the rest of the game.

Turns continue until the round ends, either by going bust or by everyone leaving.

To reset for the next round, all cards on the table added back into the deck, plus 1 artifact from the reserve pile,
and the deck is shuffled.
  
At the end of 5 rounds, the player with the most gems in their tent wins.

## Executing program

Run demo.py to see 3 bots with different strategies play against each other.
Set demo = 1 to see this demonstration run many games in quick
succession, or demo = 2 to see the game run turn-wise in greater detail.

Run interactive.py to play against a simple bot.

Run solo_turn.py, solo_backpack.py or solo_random.py to see
plots of the average score achieved by a bot playing in
single-player mode while varying the strategy used.

Run turn_vs_turn.py to see plots of the win percentage of 2 
bots playing against each other. Each bot independently
uses a turn-based strategy (leaving when the turn number
reaches the bots Turn Threshold value). Set demo = 1 or 
demo = 2 to see different levels of detail in this
pre-made demonstration.

## Authors

Ethan Watkins

## License

This project is licensed under the MIT License - see the LICENSE.txt file for details

## Acknowledgements

Incan Gold (a.k.a. Diamant) by Alan R. Moon and Bruno Faidutti, published by Schmidt Spiele et al.