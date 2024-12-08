import random

# ASCII Art
rock = '''
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
'''

paper = '''
    _______
---'   ____)____
          ______)
          _______)
         _______)
---.__________)
'''

scissors = '''
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
'''

game_images = [rock, paper, scissors]

# Prompt user for input
try:
    user_choice = int(input("What do you choose? Type 0 for Rock, 1 for Paper, or 2 for Scissors:\n"))
    if user_choice < 0 or user_choice > 2:
        print("Invalid choice. Please select 0, 1, or 2.")
    else:
        print(f"You chose:\n{game_images[user_choice]}")

        # Computer's choice
        computer_choice = random.randint(0, 2)
        print(f"Computer chose:\n{game_images[computer_choice]}")

        # Determine the winner
        if user_choice == computer_choice:
            print("It's a draw!")
        elif (user_choice == 0 and computer_choice == 2) or \
             (user_choice == 1 and computer_choice == 0) or \
             (user_choice == 2 and computer_choice == 1):
            print("You win!")
        else:
            print("You lose!")
except ValueError:
    print("Invalid input. Please enter a number (0, 1, or 2).")
