def average_median():
    user_a_or_m = input("Do you want to calculate the average or median? (a/m) ")
    if user_a_or_m == "a":
        user_input_a = input("Input list of numbers separated with spaces: ")
        numbers = []

        for number in user_input_a.split():
            numbers.append(float(number))
        average = sum(numbers) / len(numbers)
        average = round(average, 2)
        print(f"The average is {average}")
        
    elif user_a_or_m == "m":
        user_input_m = input("Input a list of numbers separated by spaces: ")
        numbers = []

        for number in user_input_m.split():
            numbers.append(float(number))
        numbers.sort()
        # Check if the length of the list is even or odd
        if len(numbers) % 2 == 0:
            median1 = numbers[len(numbers) // 2 - 1]
            median2 = numbers[len(numbers) // 2]
            median = (median1 + median2) / 2  # Calculate the average of the two middle numbers
            print(f"The median is {median}")
        else:
            median = numbers[len(numbers) // 2]
            print(f"The median is {median}")
    else:
        print("Invalid input. Please enter 'a' or 'm'.")

    repeat = input("Do you want to do another calculation? (y/n) ")
    if repeat == "y":
        average_median()
    elif repeat == "n":
        print("Goodbye!")
    else:
        print("Invalid input. Exiting.")

average_median()

