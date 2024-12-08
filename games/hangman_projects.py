import random

# ASCII art for hangman stages and logo
stages = [
    "Final stage art",
    "Stage 5 art",
    "Stage 4 art",
    "Stage 3 art",
    "Stage 2 art",
    "Stage 1 art",
    "Initial stage art",
]
logo = """
Welcome to Hangman!
"""

# Word list
word_list = [
    "abruptly", "absurd", "abyss", "affix", "askew",
    "awkward", "bagpipes", "bandwagon", "banjo", "blizzard",
    "buzzard", "cycle", "dwarves", "equip", "espionage",
    "exodus", "fishhook", "galaxy", "gossip", "jackpot",
    "jigsaw", "jukebox", "kayak", "lengths", "luxury",
    "mnemonic", "oxygen", "pajama", "quartz", "rhythm",
    "scratch", "strengths", "syndrome", "unknown", "vortex",
    "waltz", "wizard", "xylophone", "yummy", "zephyr",
]

# Game Setup
print(logo)
chosen_word = random.choice(word_list)
word_length = len(chosen_word)
lives = 6
placeholder = ["_" for _ in range(word_length)]
correct_letters = set()

print("Word to guess: " + " ".join(placeholder))

# Game Loop
game_over = False

while not game_over:
    print(f"\n{'*' * 10} {lives}/6 LIVES LEFT {'*' * 10}")
    guess = input("Guess a letter: ").lower()

    # Input validation
    if len(guess) != 1 or not guess.isalpha():
        print("Invalid input. Please enter a single alphabetical character.")
        continue

    if guess in correct_letters:
        print(f"You've already guessed '{guess}'. Try again.")
        continue

    correct_letters.add(guess)

    # Check guess and update placeholder
    if guess in chosen_word:
        for idx, letter in enumerate(chosen_word):
            if letter == guess:
                placeholder[idx] = guess
        print("Good guess!")
    else:
        print(f"'{guess}' is not in the word. You lose a life.")
        lives -= 1

    print("Word to guess: " + " ".join(placeholder))
    print(stages[lives])

    # Check for win/lose conditions
    if "_" not in placeholder:
        game_over = True
        print("Congratulations! You've guessed the word!")
    elif lives == 0:
        game_over = True
        print(f"Game Over! The word was: '{chosen_word}'. Better luck next time!")
