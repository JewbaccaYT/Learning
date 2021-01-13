# 0 for Tie; 1 for X win; 2 for O win;-1 for no win yet
# Function for checking wins based on "board" data at the end of a game
def is_win():
    x_extract = []
    o_extract = []
    is_tie = True
    x_check = False
    o_check = False

    # Checks what number is in a position on the board and adds it to a list called "extract"
    for win in list_board:
        if win == 0:
            is_tie = False
            x_extract.append(0)
            o_extract.append(0)
        elif win == 1:
            x_extract.append(1)
            o_extract.append(0)
        elif win == 2:
            x_extract.append(0)
            o_extract.append(1)

    # Checks if the "Extract" Lists match up with a possible win in the "Win_condition" List.
    for indiv_wc in win_condition:
        index = 0
        x_win = True
        o_win = True
        # If any position is proven wrong, it sets the related X or O win to false
        for board_pos in indiv_wc:
            if board_pos == 1 and x_extract[index] == 0:
                x_win = False
            if board_pos == 1 and o_extract[index] == 0:
                o_win = False
            index += 1
        if x_win:
            x_check = True
        if o_win:
            o_check = True
    # Returns different result based on the if statements above.
    # The else statement makes the game continue
    if x_check:
        return 1
    elif o_check:
        return 2
    elif is_tie:
        return 0
    else:
        return -1

# Puts X or O in each position based on player.
def Board():
    print(mapping[list_board[0]], mapping[list_board[1]], mapping[list_board[2]])
    print(mapping[list_board[3]], mapping[list_board[4]], mapping[list_board[5]])
    print(mapping[list_board[6]], mapping[list_board[7]], mapping[list_board[8]])

# Definitions and Vars
# List of all possible win scenarios in Boolean form (0 is empty, 1 is occupied).
# Had to add "extraction" function to differentiate between what number is in a position
win_condition = [[1,1,1,0,0,0,0,0,0], [1,0,0,1,0,0,1,0,0],
                 [1,0,0,0,1,0,0,0,1], [0,0,0,1,1,1,0,0,0],
                 [0,0,0,0,0,0,1,1,1], [0,1,0,0,1,0,0,1,0],
                 [0,0,1,0,0,1,0,0,1], [0,0,1,0,1,0,1,0,0]]

# Game Board
list_board = [0, 0, 0,
              0, 0, 0,
              0, 0, 0]

# Dictionary defining player X or O
mapping = {1: 'X', 2: 'O', 0: '-'}


game_ended = False
player_x = 1
player_o = 2
current_player = player_x
# Start of Game Loop
while not game_ended:
    # Checks if a position is filled
    valid = False
    place_choice = -1
    while not valid:
        try:
            place_choice = int(input('Player ' + mapping[current_player] + ' choose a spot. (A # 1-9): '))
        except ValueError:
            print("That's not a number!")
        if place_choice == -1:
            pass
        elif list_board[place_choice - 1] == 0:
            valid = True
        else:
            print('This position is taken!')

    # Show board with new X or O move
    list_board[place_choice - 1] = current_player

    Board()

    # Check for win based on the return of the Functioned Defined at the very beginning
    check_win = is_win()
    if check_win == 1:
        print('Player X Wins!')
        game_ended = True
    elif check_win == 2:
        print('Player O Wins!')
        game_ended = True
    elif check_win == 0:
        print("It's a tie!")
        game_ended = True

    # Switches Player Turns
    if current_player == player_x:
        current_player = player_o
    elif current_player == player_o:
        current_player = player_x
