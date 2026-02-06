from time import time
from itertools import product

password = input("enter your password: ")

letters = "abcdefghijklmnopqrstuvwxyz"
numbers = "123456789"
symbols = "!#$%&()*+_-"
characters = letters + numbers + symbols

start = time()
guesses = 0

for length in range(1, 13):
    for comp_guess in product(characters, repeat=length):
        guesses += 1
        if "".join(comp_guess) == password:
            end = time()
            print(f"{password=} : {guesses} guesses")
            print(f"runtime: {end - start}")
            exit()
