# Hangman Game

This is a Python implementation of the classic Hangman game, where you need to guess a hidden word by suggesting letters. Each incorrect guess costs you a life, and you have 6 lives in total. If you guess all the letters correctly before losing all your lives, you win!

## Game Rules:
- You need to guess a word, letter by letter.
- If you guess a correct letter, it will appear in the correct position in the word.
- If you guess a wrong letter, you lose one life.
- You have 6 lives in total, and the game ends either when you run out of lives or successfully guess the word.
- If you guess the word correctly before you run out of lives, you win!

## Features:
- Randomly selects a word from a predefined list.
- Displays the current state of the word, with guessed letters and underscores.
- Tracks lives and shows a "hangman" drawing as lives decrease.
- If you guess all the letters correctly, you win the game.

## How to Play:
1. **Run the Python script**:
   ```bash
   python hangman.py
