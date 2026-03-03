import time

password = input("Enter password 3 digets: ")

print("craking password")

for i in range(1000):
    guess = str(i).zfill(3)
    print("tyring", guess)
    time.sleep(0.01)

    if guess == password:
        print("password found")
        print("password =",guess)
        break

