class CoffeeMachine:
    def __init__(self):
        # Define the menu with drink types, ingredients, and prices
        self.menu = {
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
        self.resources = {
            "water": 300,  # 300 ml of water in stock
            "milk": 200,   # 200 ml of milk in stock
            "coffee": 100, # 100 grams of coffee in stock
        }

        self.profit = 0  # Variable to store accumulated profit
        self.admin_password = "admin123"  # Admin password for accessing admin mode

    def is_resource_sufficient(self, ingredients):
        for item in ingredients:
            if ingredients[item] > self.resources[item]:
                print(f"Sorry, there is not enough {item}.")
                return False
        return True

    def coin_counter(self):
        print("Insert coins please.")
        money = int(input("How many dollars? ")) * 1
        money += int(input("How many quarters? ")) * 0.25
        money += int(input("How many dimes? ")) * 0.10
        return money

    def is_transaction_successful(self, received, cost):
        if received >= cost:
            change = round(received - cost, 2)
            print(f"Here is ${change} in change.")
            self.profit += cost
            return True
        else:
            print("Sorry, not enough money. Money refunded.")
            return False

    def make_coffee(self, drink_name, order_ingredients):
        for item in order_ingredients:
            self.resources[item] -= order_ingredients[item]
        print(f"Here is your {drink_name}. Enjoy!")

    def admin_mode(self):
        print("Entering admin mode...")
        print(f"Current resources: {self.resources}")
        print(f"Total profit: ${self.profit}")
        restock = input("Would you like to restock resources? (yes/no): ").lower()
        if restock == "yes":
            self.resources["water"] += int(input("Add water: "))
            self.resources["milk"] += int(input("Add milk: "))
            self.resources["coffee"] += int(input("Add coffee: "))
            print("Resources updated successfully.")


def main():
    coffee_machine = CoffeeMachine()  # Create an instance of CoffeeMachine
    is_on = True

    while is_on:
        choice = input("What would you like? (espresso/latte/cappuccino/admin/off): ")

        if choice == "off":
            is_on = False
            print("Turning off. Goodbye!")
            break

        if choice == "admin":
            password = input("Enter admin password: ")
            if password == coffee_machine.admin_password:
                coffee_machine.admin_mode()
            else:
                print("Incorrect password. Access denied.")
            continue

        if choice not in coffee_machine.menu:
            print("Invalid choice. Please select espresso, latte, or cappuccino.")
            continue

        drink = coffee_machine.menu[choice]

        if coffee_machine.is_resource_sufficient(drink["ingredients"]):
            payment = coffee_machine.coin_counter()
            if coffee_machine.is_transaction_successful(payment, drink["cost"]):
                coffee_machine.make_coffee(choice, drink["ingredients"])

