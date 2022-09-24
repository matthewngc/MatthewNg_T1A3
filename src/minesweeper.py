# Import libraries
# from string import ascii_lowercase
import random
import os
import re

# Generate the board as a list of lists (this board is hidden from the player)
def createboard(dimensions, max_mines):
    board = [[' ' for i in range(dimensions)] for j in range(dimensions)]

    # Randomly generate mine locations and add them to the board
    mines = 0
    while mines < max_mines:
        # Generate random row and column number between 0 and the dimensions of the grid
        random_row = random.randint(0, dimensions -1)
        random_col = random.randint(0, dimensions -1)

        # Don't place a mine if the space already has a mine
        if board[random_row][random_col] == '@':
            continue
        # Otherwise, plant mine
        else:
            board[random_row][random_col] = '@'
        # Increase mine index by one
        mines += 1
    
    # Show the number of adjacent mines around each empty space
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
    for x in range(max(0,row-1), min(dimensions-1, row +1)+1):
        for y in range (max(0,col-1), min(dimensions-1,col+1)+1):
            # Don't check the space itself
            if x == row and y == col:
                continue
            # Increase adjacent_mine index by 1 for every mine around the space
            if board[x][y] == '@':
                adjacent_mines += 1
    # Return the number of adjacent mines around the space
    return adjacent_mines

# After the number of adjacent mines is counted, replace the space in the hidden board with this number
def show_adjacent_mines(dimensions, board):
    for x in range(dimensions):
        for y in range(dimensions):
            # Don't replace the spaces with a mine
            if board[x][y] == '@':
                continue
            # Replace the space with the returned number from check_mines()
            board[x][y] = check_mines(dimensions, board, x, y)

# When a space is clicked on, reveal the space
def clickspace(player_board, dimensions, newboard, row, col, input_history):
    # Add the coordinate entered to the input history to track what spaces have been clicked on
    input_history.add((row,col))
    # If the space has a mine, return False
    if newboard[row][col] == '@':
        return False
    # If the space is empty but has adjacent mines, show the number of adjacent mines and return True
    elif newboard[row][col] > 0:
        player_board[row][col] = newboard[row][col]
        return True
    # If the space is empty and has no adjacent mines, keep revealing adjacent spaces until an empty space with adjacent mines is revealed
    elif newboard[row][col] == 0:
        player_board[row][col] = newboard[row][col]
        for r in range(max(0,row-1), min(dimensions-1,row+1)+1):
            for c in range(max(0,col-1),min(dimensions-1,col+1)+1):
                if (r,c) in input_history:
                    continue
                clickspace(player_board, dimensions, newboard, r, c, input_history)
    return True

# Display the board to the player - this is what the player sees when playing the game
def display(player_board):
    gridsize = len(player_board)
    # Create top border of the board
    horizontal = '   ' + (4 * gridsize * '-') + '-'
    # Label the x-axis of the board
    toplabel = '     '
    for i in range(1, gridsize + 1):
        toplabel = toplabel + str(i) + '   '
    print(toplabel + '\n' + horizontal)
    # Label the y-axis of the board
    for idx, i in enumerate(player_board):
        row = '{0:2} |'.format(idx + 1)
        for j in i:
            row = row + ' ' + str(j) + ' |'
        print(row + '\n' + horizontal)

# Simple press to continue function
def press_to_continue():
    os.system("/bin/bash -c 'read -s -n 1 -p \"\nPress any key to continue.\"'\n")
    os.system('clear')

# Play function
def play():
    os.system("clear")
    print("Welcome to Minesweeper!")
    while True:
        difficulty = input("Please enter the difficulty you want to play on. \n"
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
            press_to_continue()
        
    # Create a new board with random mines based on user input
    newboard = createboard(dimensions, max_mines)
    #print(newboard) #DEBUG

    safe = True
    input_history = set()
    # Create a board that the player sees and updates when spaces are revealed
    player_board = [[' ' for i in range(dimensions)] for j in range(dimensions)]
    while len(input_history) < dimensions ** 2 - max_mines:
        os.system("clear")
        display(player_board)
        user_input = re.split(',(\\s)*', input("Please enter a coordinate (row,column) \n"))
        row, col = int(user_input[0])-1, int(user_input[-1])-1
        if row < 0 or row >= dimensions or col < 0 or col >= dimensions:
            print("That is not a valid coordinate - please try again!")
            press_to_continue()
            continue
        
        safe = clickspace(player_board, dimensions, newboard, row, col, input_history)
        if not safe:
            break
    # Winning message when all empty spaces are revealed
    if safe:
        print("Congrats, you won!")
        play_again = input("Would you like to play again? (y/n) \n").lower()
        if play_again == "y":
            play()
        else:
            print("Thanks for playing!")
    # Losing message when a mine is revealed
    else:
        print("Game over!")
        display(newboard)
        play_again = input("Would you like to play again? (y/n) \n").lower()
        if play_again == "y":
            play()
        else:
            print("Thanks for playing! Better luck next time!")

play()
# Flag function

# Timer function

#Play the game
#User enters a coordinate on the board
#If the user hits a mine, the game is over
#If the user hits an empty spot:
#   If there are mines around the spot, show the number of mines around the spot
#   If there are no mines around the spot, keep digging until it reaches a spot which is adjacent to mines
