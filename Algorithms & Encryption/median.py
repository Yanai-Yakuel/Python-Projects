
def median():
    choose = input("Do you want to calculate the median? (y/n) ")

    if choose == "y":
        user_in = input("Input a list of numbers separated by spaces: ")
    elif choose == "n":
        print("No median calculation")
        return  # Exit the function if the user chooses "n"
    else:
        print("Invalid input. Please enter 'y' or 'n'.")
        return

    numbers = []
    for number in user_in.split():
        numbers.append(float(number))
    numbers.sort()
    # Check if the length of the list is even or odd
    if len(numbers) % 2 == 0:
        median1 = numbers[len(numbers) // 2 - 1]
        median2 = numbers[len(numbers) // 2]
        print(f"The medians are {median1} and {median2}")
    else:
        median = numbers[len(numbers) // 2]
        print(f"The median is {median}")
    
    
median()


