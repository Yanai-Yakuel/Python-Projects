from random import randint  # Imports the randint function from the random module
from art import logo  # Imports the logo of the game from the art module

# Number of turns for each difficulty level
EASY_LEVEL_TURNS = 15
MEDIUM_LEVEL_TURNS = 10
HARD_LEVEL_TURNS = 5

# Function that checks the user's guess against the actual answer and updates the number of turns
def check_answer(user_guess, actual_answer, turns):
    if user_guess > actual_answer:
        print("Too high.")
        return turns - 1  # Decreases one turn if the guess is too high
    elif user_guess < actual_answer:
        print("Too low.")
        return turns - 1  # Decreases one turn if the guess is too low
    else:
        print(f"You got it! The answer was {actual_answer}")  # If the guess is correct

# Function to set the difficulty level
def set_difficulty():
    level = input("Set the difficulty. Type 'easy', 'medium', or 'hard': ")
    if level == "easy":
        return EASY_LEVEL_TURNS  # Returns 15 turns for "easy" difficulty
    elif level == "medium":
        return MEDIUM_LEVEL_TURNS  # Returns 10 turns for "medium" difficulty
    else:
        return HARD_LEVEL_TURNS  # Returns 5 turns for "hard" difficulty

# Function that runs the game
def game():
    print(logo)  # Displays the logo of the game
    print("Welcome to the Number Guessing Game!")  # Greeting the player
    print("I'm thinking of a number between 1 and 100.")  # Describes the objective of the game
    answer = randint(1, 100)  # Generates a random number between 1 and 100 as the correct answer

    turns = set_difficulty()  # Sets the number of turns based on the chosen difficulty

    guess = 0  # Initializes the guess variable
    while guess != answer:
        print(f"You have {turns} attempts remaining to guess the number.")  # Displays the number of attempts left
        guess = int(input("Make a guess: "))  # Prompts the user to make a guess and converts it to an integer
        turns = check_answer(guess, answer, turns)  # Calls check_answer to evaluate the guess and update turns
        if turns == 0:
            print("You've run out of guesses, you lose.")  # If there are no turns left, the player loses
            return
        elif guess != answer:
            print("Guess again.")  # If the guess is incorrect, asks the player to try again

# Starts the game
game()
