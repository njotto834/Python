#2 Simple guessing games: In guess(x), the computer has a random secret number that the user tries to guess. In computer_guess(x),
#the computer is trying to guess a secret number that the user knows.

import random

def guess(x):
    random_number = random.randint(1, x)
    guess = int(input(f"Guess a number between 1 and {x}: "))
    while (guess != random_number):
        if (guess < random_number):
            guess = int(input("Guess a larger number:"))
        elif(guess > random_number):
            guess = int(input("Guess a smaller number:"))
    print("Correct!")

def computer_guess(x):
    low = 1
    high = x
    feedback = ''
    while (feedback != 'c'):
        if low != high:
            guess = random.randint(low, high)
        else:
            guess = low
        print(f"Guess: {guess}")
        feedback = input(f"Is {guess} too high (h), too low (l), or correct(c)?").lower()
        if feedback == 'h':
            high = guess - 1
        elif feedback == 'l':
            low = guess + 1
    print("The computer guessed your number correctly!")
        
# guess(10)
# computer_guess(10)


