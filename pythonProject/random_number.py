import random

computers_choice = random.randint(1,100)

#players_guess = int(input("What is my number? "))
has_guessed = False

while not(has_guessed):
    players_guess = int(input("What is my number? "))
    if players_guess < computers_choice:
        print('Too Low')
    elif players_guess > computers_choice:
        print('Too High')
    elif players_guess == computers_choice:
        print('You Got It!')
        has_guessed = True


