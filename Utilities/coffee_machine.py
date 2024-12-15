MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

profit = 0

admin_password = "admin123"

def is_resource_sufficient(ingredients):
    for item in ingredients:
        if ingredients[item] > resources[item]:
            print(f"Sorry, there is not enough {item}.")
            return False
    return True

def coin_counter():
    print("Insert coins please.")
    money = int(input("How many dollars? ")) * 1
    money += int(input("How many quarters? ")) * 0.25
    money += int(input("How many dimes? ")) * 0.10
    money += int(input("How many nickels? ")) * 0.05
    return money

def is_transaction_successful(received, cost):
    if received >= cost:
        change = round(received - cost, 2)
        print(f"Here is ${change} in change.")
        global profit
        profit += cost
        return True
    else:
        print("Sorry, not enough money. Money refunded.")
        return False

def make_coffee(drink_name, order_ingredients):
    for item in order_ingredients:
        resources[item] -= order_ingredients[item]
    print(f"Here is your {drink_name}. Enjoy!")

def admin_mode():
    print("Entering admin mode...")
    print(f"Current resources: {resources}")
    print(f"Total profit: ${profit}")
    restock = input("Would you like to restock resources? (yes/no): ").lower()
    if restock == "yes":
        resources["water"] += int(input("Add water: "))
        resources["milk"] += int(input("Add milk: "))
        resources["coffee"] += int(input("Add coffee: "))
        print("Resources updated successfully.")

is_on = True

while is_on:
    choice = input("What would you like? (espresso/latte/cappuccino/admin/off): ")

    if choice == "off":
        is_on = False
        print("Turning off. Goodbye!")
        break

    if choice == "admin":
        password = input("Enter admin password: ")
        if password == admin_password:
            admin_mode()
        else:
            print("Incorrect password. Access denied.")
        continue

    if choice not in MENU:
        print("Invalid choice. Please select espresso, latte, or cappuccino.")
        continue

    drink = MENU[choice]

    if is_resource_sufficient(drink["ingredients"]):
        payment = coin_counter()
        if is_transaction_successful(payment, drink["cost"]):
            make_coffee(choice, drink["ingredients"])
