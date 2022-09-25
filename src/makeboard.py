"""Import random module"""
import random

# Generate the board as a list of lists (this board is hidden from the player)
def createboard(dimensions, max_mines):
    """Function to create a new board and add mines"""
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
    """Function to check the number of adjacent mines around each space"""
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

# After the number of adjacent mines is counted, replace the space on the board with this number
def show_adjacent_mines(dimensions, board):
    """Function that assigns the adjacent mines value to the empty spaces"""
    for x in range(dimensions):
        for y in range(dimensions):
            # Don't replace the spaces with a mine
            if board[x][y] == '@':
                continue
            # Replace the space with the returned number from check_mines()
            board[x][y] = check_mines(dimensions, board, x, y)

# Display the board to the player - this is what the player sees when playing the game
def display_board(player_board):
    """Function to display the board to the player"""
    dim = len(player_board)
    # Create top border of the board
    topborder = '   ' + (4 * dim * '-') + '-'
    # Label the x-axis of the board
    xlabel = '     '
    for i in range(1, dim + 1):
        xlabel = xlabel + str(i) + '   '
    print(xlabel + '\n' + topborder)
    # Label the y-axis of the board
    for idx, i in enumerate(player_board):
        row = '{0:2} |'.format(idx + 1)
        for j in i:
            row = row + ' ' + str(j) + ' |'
        print(row + '\n' + topborder)
