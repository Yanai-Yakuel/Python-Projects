# Define the menu with drink types, ingredients, and prices
MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,  # 50 ml of water
            "coffee": 18,  # 18 grams of coffee
        },
        "cost": 1.5,  # Price of espresso
    },
    "latte": {
        "ingredients": {
            "water": 200,  # 200 ml of water
            "milk": 150,   # 150 ml of milk
            "coffee": 24,  # 24 grams of coffee
        },
        "cost": 2.5,  # Price of latte
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,  # 250 ml of water
            "milk": 100,   # 100 ml of milk
            "coffee": 24,  # 24 grams of coffee
        },
        "cost": 3.0,  # Price of cappuccino
    }
}

# Define the available resources (inventory)
resources = {
    "water": 300,  # 300 ml of water in stock
    "milk": 200,   # 200 ml of milk in stock
    "coffee": 100, # 100 grams of coffee in stock
}

# Variable to store accumulated profit
profit = 0

# Admin password for accessing admin mode
admin_password = "admin123"

# Function that checks if there are enough resources to make a drink
def is_resource_sufficient(ingredients):
    for item in ingredients:  # Loop through each required ingredient for the drink
        if ingredients[item] > resources[item]:  # If the requested amount is greater than what's available
            print(f"Sorry, there is not enough {item}.")  # Notify that there is not enough of the item
            return False  # Return False if any ingredient is insufficient
    return True  # Return True if all ingredients are sufficient

# Function that handles the coin input for payment
def coin_counter():
    print("Insert coins please.")  # Ask the user to insert coins
    money = int(input("How many dollars? ")) * 1  # Calculate the amount in dollars
    money += int(input("How many quarters? ")) * 0.25  # Add the value of quarters
    money += int(input("How many dimes? ")) * 0.10  # Add the value of dimes
    return money  # Return the total amount of money inserted

# Function that checks if the transaction is successful (enough money is given)
def is_transaction_successful(received, cost):
    if received >= cost:  # If the received money is greater than or equal to the cost
        change = round(received - cost, 2)  # Calculate the change to be returned
        print(f"Here is ${change} in change.")  # Inform the user of the change
        global profit  # Access the global profit variable
        profit += cost  # Add the cost of the drink to the profit
        return True  # Return True if the transaction is successful
    else:
        print("Sorry, not enough money. Money refunded.")  # Notify the user if the money is insufficient
        return False  # Return False if the transaction is not successful

# Function to make the coffee and update resources
def make_coffee(drink_name, order_ingredients):
    for item in order_ingredients:  # Loop through the ingredients
        resources[item] -= order_ingredients[item]  # Deduct the ingredients from the resources
    print(f"Here is your {drink_name}. Enjoy!")  # Inform the user that their drink is ready

# Admin mode function
def admin_mode():
    print("Entering admin mode...")  # Inform the user that admin mode is entered
    print(f"Current resources: {resources}")  # Show the current resources available
    print(f"Total profit: ${profit}")  # Show the total profit so far
    restock = input("Would you like to restock resources? (yes/no): ").lower()  # Ask if they want to restock
    if restock == "yes":  # If the user wants to restock
        resources["water"] += int(input("Add water: "))  # Add water to the resources
        resources["milk"] += int(input("Add milk: "))  # Add milk to the resources
        resources["coffee"] += int(input("Add coffee: "))  # Add coffee to the resources
        print("Resources updated successfully.")  # Inform the user that the resources have been updated

# Main program loop
is_on = True

while is_on:
    # Ask the user what drink they would like to order
    choice = input("What would you like? (espresso/latte/cappuccino/admin/off): ")

    if choice == "off":  # If the user wants to turn off the machine
        is_on = False  # Exit the loop
        print("Turning off. Goodbye!")  # Inform the user that the machine is turning off
        break

    if choice == "admin":  # If the user selects admin mode
        password = input("Enter admin password: ")  # Prompt for the admin password
        if password == admin_password:  # If the entered password is correct
            admin_mode()  # Enter admin mode
        else:
            print("Incorrect password. Access denied.")  # If the password is incorrect, deny access
        continue  # Continue to the next iteration of the loop

    if choice not in MENU:  # If the user selects an invalid option
        print("Invalid choice. Please select espresso, latte, or cappuccino.")  # Inform the user of invalid input
        continue  # Continue to the next iteration of the loop

    # Get the selected drink's recipe and cost
    drink = MENU[choice]

    # Check if there are enough resources for the selected drink
    if is_resource_sufficient(drink["ingredients"]):
        payment = coin_counter()  # Get the money inserted by the user
        # If the transaction is successful, make the coffee
        if is_transaction_successful(payment, drink["cost"]):
            make_coffee(choice, drink["ingredients"])
