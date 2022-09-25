"""Import press to continue function from prompts file"""
from prompts import press_to_continue

# When a space is clicked on, reveal the space
def show_space(player_board, dimensions, newboard, row, col, input_history):
    """Function to reveal the space entered by the player"""
    if player_board[row][col] == 'F':
        print("There is a flag here! Type 'F' after the coordinate to remove the flag (row,col,F).")
        press_to_continue()
        return True
    # Add the coordinate entered to the input history to track what spaces have been clicked on
    input_history.add((row,col))
    # If the space has already been revealed, show error message and return True
    if player_board[row][col] == newboard[row][col]:
        print("You have already revealed this spot! Please enter a different coordinate.")
        press_to_continue()
        return True
    # If the space has a mine, return False
    if newboard[row][col] == '@':
        return False
    # If the space is empty but has adjacent mines, show the number of adjacent mines
    if newboard[row][col] > 0:
        player_board[row][col] = newboard[row][col]
        return True
    # If the space is empty and has no adjacent mines, keep revealing adjacent spaces until
    # an empty space with adjacent mines is revealed
    if newboard[row][col] == 0:
        player_board[row][col] = newboard[row][col]
        for r in range(max(0,row-1), min(dimensions-1,row+1)+1):
            for c in range(max(0,col-1),min(dimensions-1,col+1)+1):
                if (r,c) in input_history:
                    continue
                if player_board[r][c] == 'F':
                    continue
                show_space(player_board, dimensions, newboard, r, c, input_history)
    return True

# Place a flag on a space that may be a mine
def place_flag(player_board, row, col):
    """Function to place a flag"""
    # If the space has already been revealed or already has a flag, prevent a flag from being placed
    if player_board[row][col] != ' ' and player_board[row][col] != 'F':
        print("You can't put a flag here!")
    # If the space already has a flag, remove the flag
    elif player_board[row][col] == 'F':
        player_board[row][col] = ' '
    # If the space does not have a flag, place a flag
    else:
        player_board[row][col] = 'F'
