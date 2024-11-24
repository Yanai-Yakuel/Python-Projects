# Number Guessing Game

This is a simple Python game where the player needs to guess a randomly chosen number between 1 and 100. The player can choose the difficulty level which determines the number of attempts allowed to guess the number.

## Features:
- **Random number generation**: The program generates a random number between 1 and 100.
- **Difficulty levels**: The player can choose between three difficulty levels:
  - **Easy**: 15 attempts.
  - **Medium**: 10 attempts.
  - **Hard**: 5 attempts.
- **Hints**: After each guess, the program will tell you if the guess is too high or too low.
- **Game Over**: If the player runs out of attempts, the game ends, and they lose.

## How It Works:
1. The program selects a random number between 1 and 100.
2. The player is prompted to select a difficulty level, which determines the number of turns.
3. The player makes guesses to find the correct number.
4. After each guess, the program provides feedback whether the guess was too high, too low, or correct.
5. The player has to guess the number within the number of allowed turns. If the player runs out of turns, they lose.

## How to Use:
1. **Run the script**:
   ```bash
   python guessing_game.py
