from time import time
from itertools import product

user_password = input("enter your password know how strong it is:")

score = 0 
password = user_password

if len(password) >= 12:
    score += 3
elif len(password) >= 8:
    score += 2 
else:
    score += 1


if any(c.islower() for c in password):
    score += 1

if any(c.isupper() for c in password):
    score += 1

if any(c.isdigit() for c in password):
    score += 1


if any(c in "!@#$%^&*()-_+=" for c in password):
    score += 1    



if score >= 7:
    print("password is good!")
elif score >= 5:
    print("passwors is mid")
else:
    print("weak!!!")