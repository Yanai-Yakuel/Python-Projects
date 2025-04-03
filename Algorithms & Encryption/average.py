def average():
    user_input = input("input list of numbers separate with spaces ")
    list = []

    for number in user_input.split():
        list.append(float(number))
    average = sum(list) / len(list)
    round(average, 2)
    print(f"The average is {average}")
average()
    

