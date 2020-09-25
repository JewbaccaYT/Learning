import random

game_ended = False
# 1 = Rock; 2 = Paper, 3 = Scissors
rps = [1, 2, 3]
mapping = {1: 'Rock', 2: 'Paper', 3: 'Scissors'}
p_win = "Player Won!"
c_win = "Computer Won!"
tie = "You tied!"


while not game_ended:
    player_choice = int(input("Rock - 1, Paper - 2, or Scissors - 3?: " ))
    comp_choice = random.randint(1,3)
    print("The computer chose", mapping[comp_choice])
    if comp_choice == 1 and player_choice == 2:
        print(p_win)
    elif comp_choice == 1 and player_choice == 3:
        print(c_win)
    elif comp_choice == 1 and player_choice == 1:
        print(tie)
    elif comp_choice == 2 and player_choice == 2:
        print(tie)
    elif comp_choice == 2 and player_choice == 3:
        print(p_win)
    elif comp_choice == 2 and player_choice == 1:
        print(c_win)
    elif comp_choice == 3 and player_choice == 3:
        print(tie)
    elif comp_choice == 3 and player_choice == 2:
        print(c_win)
    elif comp_choice == 3 and player_choice == 1:
        print(p_win)
    play_again = input("Do you want to play again? Y or N: ").lower()
    if play_again == "n":
        print("Ok, it's over :(")
        game_ended = True




