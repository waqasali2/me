# -*- coding: UTF-8 -*-
"""Week 3, Exercise 4."""


import math
# import time


def binary_search(low, high, actual_number):
    """Do a binary search.

    This is going to be your first 'algorithm' in the usual sense of the word!
    you'll give it a range to guess inside, and then use binary search to home
    in on the actual_number.
    
    Each guess, print what the guess is. Then when you find the number return
    the number of guesses it took to get there and the actual number
    as a dictionary. make sure that it has exactly these keys:
    {"guess": guess, "tries": tries}
    
    This will be quite hard, especially hard if you don't have a good diagram!
    
    Use the VS Code debugging tools a lot here. It'll make understanding 
    things much easier.
    """
    tries = 0
    guess = 0

    while True: #basically means loop indefinitely 
        list_range = list(range(low, high + 1)) #created a list that has the range of low to high, so 1 to 100 + 1
        guess = list_range[int(len(list_range)/2)] #this is the process of making the guess
        if actual_number > guess: # if the actualyu number is greater than the guess, this happens
            print(guess)
            low = guess #since our guess was less than the actual number, we have set the the new range to be from guess to high 
            tries += 1 #every time you make a guess u add one try
        elif actual_number < guess:
            print(guess)
            high = guess #since our guess was greater than the actual number, we have set the new range to be from low to guess
            tries += 1 #every time you make a guess u add one try
        else:
            return {"guess": guess, "tries": tries} #returns the the final guess (the ans) and the amount of attempts it took




if __name__ == "__main__":
    print(binary_search(1, 100, 5))
    print(binary_search(1, 100, 6))
    print(binary_search(1, 100, 95))
    print(binary_search(1, 51, 5))
    print(binary_search(1, 50, 5))
