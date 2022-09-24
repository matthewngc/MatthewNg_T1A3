# Import libraries
# from string import ascii_lowercase
import random

#Create board class with attributes dimensions and number of mines

class Board:
    def __init__(self, dimensions, max_mines):
        self.dimensions = dimensions
        self.max_mines = max_mines
        self.board = self.createboard()
        self.show_adjacent_mines()
        self.click_history = set()

    # Generate the board as a list of lists
    def createboard(self):
        board = [['0' for i in range(self.dimensions)] for j in range(self.dimensions)]

    # Randomly generate bomb locations and add them to the board
        mines = 0
        while mines < self.max_mines:
            #generate random row and column number between 0 and max number of spaces on the grid (not inclusive)
            random_row = random.randint(0, self.dimensions -1)
            random_col = random.randint(0, self.dimensions -1)
            # Ignore if the space already has a mine
            if board[random_row][random_col] == '@':
                continue
            # Otherwise, plant bomb
            else:
                board[random_row][random_col] = '@'
            # Increase mine index by one
            mines += 1
        return board


    # Check the number of mines around each space
    def check_mines(self, row, col):
        # There are a total of eight spaces to check around each space, e.g. (ignoring (0,0)):
        #   (-1,-1 ) (-1,0 ) (-1,1 )
        #   ( 0,-1 ) ( 0,0 ) ( 0,1 )
        #   ( 1,-1 ) ( 1,0 ) ( 1,1 )

        adjacent_mines = 0
        # Ranges must be in range of the board i.e. accounting for the edges of the board
        for i in range(max(0,row-1), min(self.dimensions-1, row +1)+1):
            for j in range (max(0,col-1), min(self.dimensions-1,col+1)+1):
                if i == row and j == col:
                    continue
                if self.board[row][col] == '@':
                    adjacent_mines += 1
        return adjacent_mines

    # Show the number of mines around each space
    def show_adjacent_mines(self):
        for row in range(self.dimensions):
            for col in range(self.dimensions):
                if self.board[row][col] == '@':
                    continue
                self.board[row][col]= self.check_mines(row,col)

    def click(self, row, col):
        self.click_history.add((row,col))
        if self.board[row][col] == '@':
            return False
        elif self.board[row][col] > 0:
            return True
        
        for r in range(max(0, row-1), min(self.dimensions-1, row+1)+1):
            for c in range(max(0,col-1), min(self.dimensions-1, col+1)+1):
                if (r,c) in self.click_history:
                    continue
                self.click(r,c)

    def __str__(self):
        player_board = [[' ' for i in range(self.dimensions)] for j in range(self.dimensions)]
        for row in range(self.dimensions):
            for col in range(self.dimensions):
                if (row,col) in self.click_history:
                    player_board[row][col] = str(self.board[row][col])
                else:
                    player_board[row][col] = ' '
                
# Flag function

# Timer function

#Play the game
#User enters a coordinate on the board
#If the user hits a mine, the game is over
#If the user hits an empty spot:
#   If there are mines around the spot, show the number of mines around the spot
#   If there are no mines around the spot, keep digging until it reaches a spot which is adjacent to mines
