#Hangman Game: the computer randomly selects a word from a list of words and the user guesses letters to assemble the word.

import random
from words import words
import string

def get_valid_word(words):
    word = random.choice(words)
    while '-' in word or ' ' in word:
        word = random.choice(words)
    
    return word.upper()

def hangman():
    word = get_valid_word(words)
    word_letters = set(word) #Letters in the target word
    alphabet = set(string.ascii_uppercase)
    used_letters = set() #Letters that have been guessed

    while len(word_letters) > 0:
        # #letters used
        # print("You have used these letters:", ' '.join(used_letters))

        # #what their guesses look like so far
        # word_list = [letter if letter in used_letters else '-' for letter in word]
        # print('Current word:', ' '.join(word_list))

        #getting user input
        user_letter = input("Guess a letter: ").upper()
        #If the guessed letter is a valid letter and hasn't already been guessed, add it to the 'used_letters' set
        if (user_letter in alphabet) and (user_letter not in used_letters):
            used_letters.add(user_letter)
            #if the guessed letter is in the word, remove the letter from the 'word_letters' set
            if user_letter in word_letters:
                word_letters.remove(user_letter)
        elif (user_letter in used_letters):
            print("You have already guessed that letter! Please try again.")
        else:
            print("Invalid character.")
        
        #letters used
        print("You have used these letters:", ' '.join(used_letters))

        #what their guesses look like so far
        word_list = [letter if letter in used_letters else '-' for letter in word]
        print('Current word:', ' '.join(word_list))
        
    print("You have correctly guessed the word!")

hangman()