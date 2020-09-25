# 0 for Tie; 1 for X win; 2 for O win;-1 for no win yet
def is_win():
    x_extract = []
    o_extract = []
    is_tie = True
    x_check = False
    o_check = False

    for ooss in list_board:
        if ooss == 0:
            is_tie = False
            x_extract.append(0)
            o_extract.append(0)
        elif ooss == 1:
            x_extract.append(1)
            o_extract.append(0)
        elif ooss == 2:
            x_extract.append(0)
            o_extract.append(1)

    for indiv_wc in win_condition:
        index = 0
        x_win = True
        o_win = True
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

    if x_check:
        return 1
    elif o_check:
        return 2
    elif is_tie:
        return 0
    else:
        return -1

# Definitions and Vars
win_condition = [[1,1,1,0,0,0,0,0,0], [1,0,0,1,0,0,1,0,0],
                 [1,0,0,0,1,0,0,0,1], [0,0,0,1,1,1,0,0,0],
                 [0,0,0,0,0,0,1,1,1], [0,1,0,0,1,0,0,1,0],
                 [0,0,1,0,0,1,0,0,1], [0,0,1,0,1,0,1,0,0]]

list_board = [0, 0, 0,
              0, 0, 0,
              0, 0, 0]

mapping = {1: 'X', 2: 'O', 0: '-'}

game_ended = False
player_x = 1
player_o = 2
current_player = player_x

# Start of Game Code
while not (game_ended):
    # Position Check
    valid = False
    while not (valid):
        place_choice = int(input('Player ' + mapping[current_player] + ' choose a spot. (A # 1-9): '))
        if list_board[place_choice - 1] == 0:
            valid = True
        else:
            print('This position is taken!')

    # Show board with new Pos
    list_board[place_choice - 1] = current_player

    print(mapping[list_board[0]], mapping[list_board[1]], mapping[list_board[2]])
    print(mapping[list_board[3]], mapping[list_board[4]], mapping[list_board[5]])
    print(mapping[list_board[6]], mapping[list_board[7]], mapping[list_board[8]])

    # Check for win
    check_win = is_win()
    if check_win == 1:
        print('Player X Wins! Tremendous job!')
        game_ended = True
    elif check_win == 2:
        print('Player O Wins! Such wow!')
        game_ended = True
    elif check_win == 0:
        print("It's a tie, you both suck!")
        game_ended = True

    # Switches Player Turns
    if current_player == player_x:
        current_player = player_o
    elif current_player == player_o:
        current_player = player_x
