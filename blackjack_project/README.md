# Blackjack Game

This is a Python implementation of the classic Blackjack game, where you play against the computer. The goal of the game is to get as close to 21 points as possible without exceeding it. The player and the computer are each dealt two cards at the beginning, and the player can choose to either "hit" (get another card) or "stand" (keep their current hand). The computer will continue drawing cards until it has a total of at least 17 points.

## Game Rules:
- The game uses a deck of cards with the following values:
  - Number cards (2–10) are worth their face value.
  - Jack, Queen, and King are worth 10 points.
  - Ace can be worth either 1 or 11 points, depending on the player's hand.
- The goal is to have a hand value closer to 21 than the computer, without going over 21 (busting).
- If you get exactly 21 with your first two cards, you have a "Blackjack," and you win instantly.
- The game continues until either the player or the computer wins, or both bust (go over 21).

## Features:
- Deal cards randomly from a deck.
- Player can choose to "hit" (draw another card) or "stand" (end their turn).
- The computer draws cards automatically until its score is 17 or higher.
- The game compares the player's and computer's scores to determine the winner.

## How to Play:
1. **Run the Python script**:
   ```bash
   python blackjack.py
