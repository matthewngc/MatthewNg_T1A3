# Import libraries
# from string import ascii_lowercase
import random
import os
import re

# Generate the board as a list of lists
def createboard(dimensions, max_mines):
    board = [[' ' for i in range(dimensions)] for j in range(dimensions)]

# Randomly generate bomb locations and add them to the board
    mines = 0
    while mines < max_mines:
        #generate random row and column number between 0 and max number of spaces on the grid (not inclusive)
        random_row = random.randint(0, dimensions -1)
        random_col = random.randint(0, dimensions -1)
        # Ignore if the space already has a mine
        if board[random_row][random_col] == '@':
            continue
        # Otherwise, plant bomb
        else:
            board[random_row][random_col] = '@'
        # Increase mine index by one
        mines += 1
    
    # Show the number of adjacent mines around each space
    show_adjacent_mines(dimensions, board)
    return board



# Check the number of mines around each space
def check_mines(dimensions, board, row, col):
    # There are a total of eight spaces to check around each space, e.g. (ignoring (0,0)):
    #   (-1,-1 ) (-1,0 ) (-1,1 )
    #   ( 0,-1 ) ( 0,0 ) ( 0,1 )
    #   ( 1,-1 ) ( 1,0 ) ( 1,1 )

    adjacent_mines = 0
    # Ranges must be in range of the board i.e. accounting for the edges of the board
    for r in range(max(0,row-1), min(dimensions-1, row +1)+1):
        for c in range (max(0,col-1), min(dimensions-1,col+1)+1):
            if r == row and c == col:
                continue
            if board[r][c] == '@':
                adjacent_mines += 1
    return adjacent_mines

# Show the number of mines around each space
def show_adjacent_mines(dimensions, board):
    for r in range(dimensions):
        for c in range(dimensions):
            if board[r][c] == '@':
                continue
            board[r][c] = check_mines(dimensions, board, r, c)

def clickspace(player_board, dimensions, newboard, row, col, history):
    history.add((row,col))
    if newboard[row][col] == '@':
        return False
    elif newboard[row][col] > 0:
        player_board[row][col] = newboard[row][col]
        return True
    elif newboard[row][col] == 0:
        player_board[row][col] = newboard[row][col]
        for r in range(max(0,row-1), min(dimensions-1,row+1)+1):
            for c in range(max(0,col-1),min(dimensions-1,col+1)+1):
                if (r,c) in history:
                    continue
                clickspace(player_board, dimensions, newboard, r, c, history)
    return True
def display(player_board):
    # player_board = [[' ' for i in range(dimensions)] for j in range(dimensions)]
    # for row in range(dimensions):
    #     for col in range(dimensions):
    #         if (row,col) in history:
    #             player_board[row][col] = str(player_board[row][col])
    #         else:
    #             player_board[row][col] = ' '
    gridsize = len(player_board)
    horizontal = '   ' + (4 * gridsize * '-') + '-'
    toplabel = '     '
    for i in range(1, gridsize + 1):
        toplabel = toplabel + str(i) + '   '
    print(toplabel + '\n' + horizontal)
    for idx, i in enumerate(player_board):
        row = '{0:2} |'.format(idx + 1)
        for j in i:
            row = row + ' ' + str(j) + ' |'
        print(row + '\n' + horizontal)
    # print('')
            
def play():
    print("Welcome to Minesweeper!")
    while True:
        difficulty = input("Please enter the difficulty you want to play on or 'quit' to close game. \n"
        'Easy mode: 5x5, 5 mines \n'
        'Normal mode: 10 x 10, 10 mines \n').lower()
        if difficulty == "easy":
            dimensions = 5
            max_mines = 5
            break
        elif difficulty == "normal":
            dimensions = 10
            max_mines = 10
            break
        else:
            os.system('clear')
            print("Invalid difficulty - please enter 'easy' or 'normal'")

    newboard = createboard(dimensions, max_mines)
    print(newboard)
    safe = True
    history = set()
    player_board = [[' ' for i in range(dimensions)] for j in range(dimensions)]
    # userinterface = display_board(player_board)
    while len(history) < dimensions ** 2 - max_mines:
        display(player_board)
        user_input = re.split(',(\\s)*', input("Please enter a coordinate (row,column)"))
        row, col = int(user_input[0])-1, int(user_input[-1])-1
        if row < 0 or row >= dimensions or col < 0 or col >= dimensions:
            print("Invalid - please enter a coordinate within the grid")
            continue
        
        safe = clickspace(player_board, dimensions, newboard, row, col, history)
        if not safe:
            break
    if safe:
        print("Congrats, you won!")
    else:
        print("Game over!")
        display(newboard)

play()
# Flag function

# Timer function

#Play the game
#User enters a coordinate on the board
#If the user hits a mine, the game is over
#If the user hits an empty spot:
#   If there are mines around the spot, show the number of mines around the spot
#   If there are no mines around the spot, keep digging until it reaches a spot which is adjacent to mines
