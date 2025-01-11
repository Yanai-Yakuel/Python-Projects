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

ADMIN_PASSWORD = "admin"  # הסיסמה למצב אדמין
ADMIN_MODE = False

def is_resource_sufficient(ingredients, choice):
    """Checks if there are enough resources to make a drink."""
    for item in ingredients:
        if ingredients[item] > resources[item]:
            print(f"Sorry there is not enough {item} to make {choice}")
            return False
    return True

def get_coin_input(coin_type):
   while True:
        try:
          return int(input(f"How many {coin_type}? "))
          break
        except ValueError:
            print("Invalid input. Please enter a number")

def coin_counter():
    """Prompts user for coin input and returns the total money."""
    print("Insert coins please ")
    money = get_coin_input("doller") * 1
    money += get_coin_input("quarters") * 0.25
    money += get_coin_input("dimes") * 0.10
    money += get_coin_input("nickles") * 0.05
    return money

def is_transaction_successful(received, cost):
    """Checks if the transaction is successful and updates profit."""
    if received >= cost:
        change = round(received - cost, 2)
        print(f"Here is ${change} in change. ")
        global profit
        profit += cost
        return True
    else:
        print("Sorry not enough money. Money refunded.")
        return False

def make_coffee(drink_name, order_ingredients):
    """Makes the coffee, subtracting resources and printing a confirmation."""
    for item in order_ingredients:
        resources[item] -= order_ingredients[item]
    print(f"Here is your {drink_name}. Enjoy!")

def enter_admin_mode():
    """Tries to enter admin mode, and sets the ADMIN_MODE to true if password is correct."""
    global ADMIN_MODE
    password = input("Enter admin password: ")
    if password == ADMIN_PASSWORD:
        print("Admin mode activated")
        ADMIN_MODE = True
        return True
    else:
        print("Incorrect password.")
        return False
def exit_admin_mode():
    """Exit admin mode by setting the ADMIN_MODE to false"""
    global ADMIN_MODE
    ADMIN_MODE = False
    print("Admin mode deactivated.")

def admin_report():
      while True:
        report_type = input("What report do you want? (report/profit/exit): ").lower()
        if report_type == "report":
             print(f"Water: {resources['water']}ml")
             print(f"Milk: {resources['milk']}ml")
             print(f"Coffee: {resources['coffee']}g")
             print(f"Profit: ${profit}")
        elif report_type == "profit":
             print(f"Profit: ${profit}")
        elif report_type == "exit":
              break
        else:
              print("Invalid report type. Please select report, profit, or exit.")

is_on = True

while is_on:
    choice = input("What would you like? (espresso/latte/cappuccino/admin/off): ").lower()

    if choice == "off":
        is_on = False
        print("Turning off. Goodbye!")
        break

    if choice == "admin":
        if not ADMIN_MODE:
          if enter_admin_mode():
             admin_report()
        else:
           exit_admin_mode()
        continue  # Skip to the next loop iteration

    if choice not in MENU:
        print("Invalid choice. Please select espresso, latte, cappuccino, admin, or off.")
        continue

    drink = MENU[choice]

    if is_resource_sufficient(drink["ingredients"], choice):
      payment = coin_counter()
      if is_transaction_successful(payment, drink["cost"]):
          make_coffee(choice, drink["ingredients"])
    if choice not in MENU:
        print("Invalid choice. Please select espresso, latte, cappuccino, report, or off.")
        continue

    drink = MENU[choice]

    if is_resource_sufficient(drink["ingredients"], choice):
      payment = coin_counter()
      if is_transaction_successful(payment, drink["cost"]):
          make_coffee(choice, drink["ingredients"])

