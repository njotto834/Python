#Simple Rock-Paper-Scissors game against the computer

import random

def play():
    user = input("Input 'r' for rock, 'p' for paper, 's' for scissors: ")
    computer = random.choice(['r', 'p', 's'])

    if (user == computer):
        return 'It\'s a tie'
    elif (is_win(user, computer)):
        return 'You Won!'

    return 'You Lost'
    
def is_win(player, opponent):
    #returns true if the player wins
    if (player == 'p' and opponent == 'r') or (player == 'r' and opponent == 's') or (player == 's' and opponent == 'p'):
        return True
    else:
        return False

print(play())

