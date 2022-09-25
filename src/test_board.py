"""Import modules"""
import random
from makeboard import createboard, check_mines
from controls import show_space

def test_createboard():
    """Test createboard() function"""
    # Set test dimension parameter as between 5 and 10
    dimensions = random.randint(5,10)
    # Max mines must be greater than 0 and less than the total number of spaces
    max_mines = random.randint(1,dimensions**2-1)
    # Tests that the board returned by this function NOT EMPTY for any given parameters
    assert createboard(dimensions,max_mines) != [[' ' for i in range(dimensions)] for j in range(dimensions)]

def test_show_space():
    """Test show_space function"""
    # Default parameters
    dimensions = 5
    player_board = [[' ' for i in range(dimensions)] for j in range(dimensions)]
    input_history = set()
    # Dummy board that has a mine at (0, 0) only
    newboard = [['@',1,0,0,0],
                [1,1,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0],
                [0,0,0,0,0]]
    # Set row & col to the board position with the mine
    row = 0
    col = 0
    # Tests that the function will return False when the input coordinate has a mine
    assert show_space(player_board, dimensions, newboard, row, col, input_history) is False
    # Tests that the function will return True when the input coordinate does not have a mine
    for i in range(1,5):
        for j in range(1,5):
            assert show_space(player_board, dimensions, newboard, row+i, col+j, input_history) is True

def test_check_mines():
    # Default dimension parameter
    dimensions = 5
    # Dummy board with mine located at row = 2, col = 2
    board = [[0,0,0,0,0],
            [0,0,0,0,0],
            [0,0,'@',0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]]
    # Mine location
    row = 2
    col = 2
    # Tests that all 8 spaces around the mine will return adjacent_mine = 1
    for i in range(1,2):
        for j in range(1,2):
            assert check_mines(dimensions, board, row+i, col+j) == 1
