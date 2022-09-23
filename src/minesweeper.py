# Import libraries
from string import ascii_lowercase
import random

#Create Minesweeper board

def createboard():
    board = [[0 for i in range(dimensions)] for j in range(dimensions)]

    # Randomly generate bomb locations and add them to the board
    mines = 0
    while mines < max_mines:
        #generate random number between 0 and max number of spaces on the grid (not inclusive)
        random_mine = random.randint(0, max_mines**2 -1)
        # Find row number by dividing dimension size by the random number and finding the quotient
        row = random_mine // dimensions
        # Then find the column number by using the remainder of the above division
        col = random_mine % dimensions
        # Ignore if the space already has a mine
        if [row][col] == '@':
            continue
        # Otherwise, plant bomb
        else:
            board[row][col] = '@'
        # Increase mine index by one
        mines += 1


# grid = []
# gridsize = 9

# currgrid = [[' ' for i in range(gridsize)] for i in range(gridsize)]

# getgrid(currgrid)

#Place mines randomly on the board

# Dig function

# Flag function

# Timer function

#Play the game
#User enters a coordinate on the board
#If the user hits a mine, the game is over
#If the user hits an empty spot:
#   If there are mines around the spot, show the number of mines around the spot
#   If there are no mines around the spot, keep digging until it reaches a spot which is adjacent to mines
