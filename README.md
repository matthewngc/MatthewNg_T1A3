# Matthew Ng - T1A3 Terminal Application

## Referenced Sources (R3)

## Link to Source Control Repository (R4)

### [Github Repo](https://github.com/matthewngc/MatthewNg_T1A3)

### [Presentation Video]()

### [Presentation Slides]()

## Style Guide (R5)

## Overview of Terminal Application

The purpose of this terminal application is to recreate the popular game of minesweeper that can be played within the terminal.

## Features (R6)

### Feature 1: Adjacent Mines

At the core of a game of Minesweeper, the most essential feature is the display of adjacent mines for any given empty space. By showing these adjacent mines as hints, a player is able to complete a game of Minesweeper without landing on any mines.

To understand how this feature is to be implemented, it is important to understand the logic behind how these checks are performed.

For any given space ( 0 , 0 ) on a Minesweeper board, the surrounding spaces are defined as follows:

       (-1,-1 ) (-1,0 ) (-1,1 )
       ( 0,-1 ) ( 0,0 ) ( 0,1 )
       ( 1,-1 ) ( 1,0 ) ( 1,1 )

where ( 0 , 0 ) is the space that the player has selected.

In order to find the mines adjacent to this uncovered space, a check is performed on the four cardinal directions (North, East, South, West), as well as the four diagonals, to see whether these spaces contain a mine.

A count is performed for each adjacent space where a mine is located, and the total of this count is assigned to the space that the player has revealed, for a value of 0 to 8.

To replicate this check in the terminal application, the following function is used:

```python
    def check_mines(dimensions, board, row, col):
        adjacent_mines = 0
        for x in range(max(0,row-1), min(dimensions-1, row +1)+1):
            for y in range (max(0,col-1), min(dimensions-1,col+1)+1):
                if x == row and y == col:
                    continue
                if board[x][y] == '@':
                    adjacent_mines += 1
        return adjacent_mines
```

Per the above function, the initial value of adjacent mines is set to zero. The proceeding 'for' loops check the eight adjacent spaces around any given space for mines. A max and min function has been included in the range to ensure that the checks stay within the bounds of the board, specifically pertaining to the spaces on the edge of the board. The count of adjacent mines is then indexed by 1 for each mine that is present in the adjacent cells. Finally, the value is returned.

The returned value is then assigned to the corresponding space on the board using the following function:

```python
def show_adjacent_mines(dimensions, board):
    for x in range(dimensions):
        for y in range(dimensions):
            if board[x][y] == '@':
                continue
            board[x][y] = check_mines(dimensions, board, x, y)
```

The 'for' loops in the above function will ensure that each empty space on the board is assigned a value representing the number of mines adjacent to this space.

### Feature 2: Recursive Digging

One of the quality-of-life features of the original Minesweeper game is the ability to recursively dig through empty tiles until an empty tile that is adjacent to mines is revealed. Upon understanding the logic behind Feature 1, it is relatively straightforward to achieve this recursive algorithm within the show_space function using the following code:

```python
    if newboard[row][col] == 0:
        player_board[row][col] = newboard[row][col]
        for r in range(max(0,row-1), min(dimensions-1,row+1)+1):
            for c in range(max(0,col-1),min(dimensions-1,col+1)+1):
                if (r,c) in input_history:
                    continue
                if player_board[r][c] == 'F':
                    continue
                clickspace(player_board, dimensions, newboard, r, c, input_history)
    if newboard[row][col] > 0:
        player_board[row][col] = newboard[row][col]
        return True    
```

In essense, the above code snippet states that if a space is revealed and the value is zero, then the show_space function will be repeatedly performed on the adjacent tiles in each direction until a tile with adjacent mines, that is, any empty tiles with a value greater than zero, is reached, at which point the loop ends and the player is prompted to select another tile.

### Feature 3: Flags

### Feature 4: In-Game Timer

## Implementation Plan (R7)

## Installation Instructions (R8)

