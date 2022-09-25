# Matthew Ng - T1A3 Terminal Application

---

## Table of Contents

[**Link to Source Control Repository (R4)**](#link-to-source-control-repository-r4)

[**Overview of Terminal Application**](#overview-of-terminal-application)

[**Flow Chart**](#flow-chart)

[**Features (R6)**](#features-r6)

- [Feature 1: Revealing Spaces](#feature-1-revealing-spaces)
- [Feature 2: Adjacent Mines](#feature-2-adjacent-mines)
- [Feature 3: Recursive Digging](#feature-3-recursive-digging)
- [Feature 4: Flags](#feature-4-flags)
- [Feature 5: In-Game Timer](#feature-5-in-game-timer)
- [Feature 6: Difficulty Setting](#feature-6-difficulty-setting)

[**Function Tests**](#function-tests)

[**Implementation Plan (R7)**](#implementation-plan-r7)

[**Installation Instructions**](#installation-instructions-r8)

[**Style Guide (R5)**](#style-guide-r5)

[**Referenced Sources (R3)**](#referenced-sources-r3)


## Link to Source Control Repository (R4)

### [Github Repo](https://github.com/matthewngc/MatthewNg_T1A3)

### [Presentation Video](https://youtu.be/PrDPhP2G2vY)

### [Presentation Slides](ppt/slides.pdf)

## Overview of Terminal Application

The purpose of this terminal application is to recreate the popular game of Minesweeper that can be played within the terminal. The goal of Minesweeper is to reveal all the empty tiles on a grid, without revealing any mines that are hidden throughout the grid. The game ends when all the empty tiles are cleared on the grid, or when a mine is revealed.

This terminal application will aim to reproduce these key game mechanics, as well as implement features such as the ability to place flags, a functional timer, and multiple difficulty options.

## Flow Chart

![Flow Chart](docs/flowchart.png)

## Features (R6)

### **Feature 1: Revealing Spaces**

The premise of a Minesweeper game is to reveal all the empty spaces on the grid without hitting a single mine. As such, the feature that forms the basis of the game is the functionality to reveal a specific space based on a user input.

In order to implement this feature, there are two boards that is generated when the game starts. The first board is hidden from the player, and shows all the locations of the mines and empty spaces. The second board is the one that the player will be playing on, and will constantly update after every user input. Both boards are represented by a list of lists, and the dimensions correspond such that the coordinates of each space match between the two boards.

The core of this function is per below:

```python
def show_space(player_board, dimensions, newboard, row, col, input_history):
    input_history.add((row,col))
    if player_board[row][col] == newboard[row][col]:
        print("You have already revealed this spot! Please enter a different coordinate.")
        press_to_continue()
        return True
    if newboard[row][col] == '@':
        return False
    if newboard[row][col] > 0:
        player_board[row][col] = newboard[row][col]
        return True
    if newboard[row][col] == 0:
        player_board[row][col] = newboard[row][col]
        return True
```

Essentially, the above function matches the coordinates entered by the player with the respective value on the hidden board. If this value is not a mine, the respective position on the player board is replaced with this value, and the game will continue. However, if the value is a mine (represented by '@'), the loop within the play function will break, and the game will end.

### *Error Handling: If user enters an invalid coordinate*

The play function uses a 'while' loop to repeatedly prompt the player to enter a coordinate until a valid coordinate is input. If the user enters an invalid coordinate, the following if statements will return an error prompt based on the user input:

1. **If too many coordinates are entered:**

    ```python
            user_input = re.split(r"[-;,.\s]\s*", input("Please enter a coordinate (row,column). \nTo place a flag, type F after the coordinate (row,column,F) \n"))
            if len(user_input) > 3:
                print("You've entered too many coordinates! Please try again.")
                press_to_continue()
                continue
    ```

    The application returns the message "You've entered too many coordinates! Please try again."

2. **If too few coordinates are entered:**

    ```python
            if len(user_input) < 2:
                print("You haven't entered enough coordinates! Please try again.")
                press_to_continue()
                continue
    ```

    The application returns the message "You haven't entered enough coordinates! Please try again."

3. **If a coordinate that is out of range is entered, or the coordinate are not integers:**

    ```python
            try:
                row, col, flag = int(user_input[0])-1, int(user_input[1])-1, user_input[-1]
            except ValueError:
                print("That is not a valid coordinate - please try again!")
                press_to_continue()
                continue
            if len(user_input) == 2:
                if row < 0 or row >= dimensions or col < 0 or col >= dimensions:
                    print("That is not a valid coordinate - please try again!")
                    press_to_continue()
                    continue
    ```

    The application returns the message "That is not a valid coordinate - please try again!"

### *Error Handling: User enters a coordinate that is already revealed or flagged*

There are two if statements included within the show_space function that will prompt a message when the player attempts to reveal a space that has already been revealed, or a space that is flagged. See below for these two if statements:

```python
    if player_board[row][col] == 'F':
        print("There is a flag here! Type 'F' after the coordinate to remove the flag (row,col,F).")
        press_to_continue()
        return True
    if player_board[row][col] == newboard[row][col]:
        print("You have already revealed this spot! Please enter a different coordinate.")
        press_to_continue()
        return True
```

### *Error Handling: Player enters a space in front of the coordinate*

A ValueError occurs if there is a space preceding the coordinate. This is due to the nature of the re.split method, which will return the space as an empty string, i.e. if the player inputs ' 3, 3, F', using re.split on the input will return the list [' ', '3', '3,', 'F']. As such, the following code is used to remove the empty string in the user_input list:

```python
    user_input = list(filter(None, user_input))
```

### **Feature 2: Adjacent Mines**

At the core of a game of Minesweeper, the most essential feature is the display of adjacent mines for any given empty space. By showing these adjacent mines as hints, a player is able to complete a game of Minesweeper without landing on any mines.

To understand how this feature is to be implemented, it is important to understand the logic behind how these checks are performed.

For any given space ( 0 , 0 ) on a Minesweeper board, the surrounding spaces are defined as follows:

```python
       (-1,-1 ) (-1,0 ) (-1,1 )
       ( 0,-1 ) ( 0,0 ) ( 0,1 )
       ( 1,-1 ) ( 1,0 ) ( 1,1 )
```

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

### **Feature 3: Recursive Digging**

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
                show_space(player_board, dimensions, newboard, r, c, input_history)
    if newboard[row][col] > 0:
        player_board[row][col] = newboard[row][col]
        return True    
```

In essence, the above code snippet states that if a space is revealed and the value is zero, then the show_space function will be repeatedly performed on the adjacent tiles in each direction until a tile with adjacent mines, that is, any empty tiles with a value greater than zero, is reached, or a flag is reached, at which point the loop ends and the player is prompted to select another tile.

### **Feature 4: Flags**

Another user-friendly feature of the original Minesweeper game is the flagging function, which allows the player to place a flag on the spaces where they believe a mine is located. This flagging feature is not only useful as a visual aid to assist the player in completing the game, but also prevents the player from accidentally selecting a tile that they know is a mine.

When played within the terminal where the player is prone to misinputs, this feature is especially practical from a quality-of-life point of view. The code of the flag feature is built into the place_flag function as below:

```python
def place_flag(player_board, row, col):
    if player_board[row][col] != ' ' and player_board[row][col] != 'F':
        print("You can't put a flag here!")
    elif player_board[row][col] == 'F':
        player_board[row][col] = ' '
    else:
        player_board[row][col] = 'F'
```

Per the above function, the player can place a flag on a space by including an 'F' after the coordinate of the space. They can also remove a flag by repeating this step.

### *Error Handling: If the player attempts to reveal a flagged space*

Considerations have been included in the show_space function to prevent a flagged tile from being revealed by using the below if statement:

```python
    if player_board[row][col] == 'F':
        print("There is a flag here! Type 'F' after the coordinate to remove the flag (row,col,F).")
        press_to_continue()
        return True
```

### **Feature 5: In-Game Timer**

An in-game timer has also been implemented in this terminal application to allow players to see how long it took for them to complete the game. The timer is achieved by importing the time() method from the time module and using the following code within the play function:

```python
    start_time = time.time()

    if emptyspace:
        os.system("clear")
        print("Congrats, you won!")
        display(newboard)
        print(f"Your time was {int(time.time()-start_time)} seconds!")
        replay()
```

The time() method returns the time in seconds since the epoch (January 1, 1970, 00:00:00 (UTC)). By assigning a variable to time.time() when the Minesweeper game is initiated and taking the difference between this variable and the time.time() at which the game is completed, a timer function can be replicated.

### **Feature 6: Difficulty Setting**

The final feature of this terminal application is a difficulty setting, which is common in many variations of Minesweeper. This difficulty setting is based on an input from the user confirming which difficulty they would like to play on. The difficulty selected will define the paramaters at which the board is generated, varying in the dimensions of the board and the number of mines placed on the board. For now, there are only two difficulty levels available to be played on this version of the terminal application.

The code for this feature is as follows:

```python
    while True:
        difficulty = input("Please enter the difficulty you want to play on./n"
        'Easy mode: 5x5, 4 mines \n'
        'Normal mode: 10 x 10, 10 mines \n').lower()
        if difficulty == "easy":
            dimensions = 5
            max_mines = 4
            break
        elif difficulty == "normal":
            dimensions = 10
            max_mines = 10
            break
        else:
            os.system('clear')
            print("Invalid difficulty - please enter 'easy' or 'normal'")
            press_to_continue()
            continue
```

Per above, the parameters of dimensions and max_mines varies depending on the difficulty that the user selects. These parameters are subsequently passed into several functions in order to generate the board and continue through the game.

### *Error Handling: If the player enters a difficulty that is invalid*

As shown in the code snippet above, the input function is nested within a 'while' loop in order to repeatedly prompt the player to enter a difficulty until a valid difficulty is entered.

## Function Tests

Three tests have been designed and performed to ensure that the main features of the application are running as expected. Pytest was used to perform these tests with no exceptions.

![Pytest Results](docs/pytest.PNG)

### **Test 1: createboard() function creates a board that is not empty**

The first test is performed on the createboard() function, and checks that it returns board that is not an empty board. This check ensures that the mines and adjacent_mines values are assigned to the board.

This function is one of the most crucial parts of the application as it generates the initial board that the game will be based on. As such, it is important for this function to work as expected.

The test function is as follows:

```python
def test_createboard():
    """Test createboard() function"""
    # Set test dimension parameter as between 5 and 10
    dimensions = random.randint(5,10)
    # Max mines must be greater than 0 and less than the total number of spaces
    max_mines = random.randint(1,dimensions**2-1)
    # Tests that the board returned by this function NOT EMPTY for any given parameters
    assert createboard(dimensions,max_mines) != [[' ' for i in range(dimensions)] for j in range(dimensions)]
```

### **Test 2: show_space() function returns the appropriate value**

The second test is performed on the show_space() function, and checks that for the coordinate with a mine, the function returns False, and for coordinates that do not have a mine, the function returns True.

This function is the means through which the player interacts with the game, and is one of the essential functions of Feature 1.

The test function is as follows:

```python
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
```

### **Test 3: show_adjacent_mines() function returns the correct value**

The third test is performed on the show_adjacent_mines function, and checks that for a dummy board with one mine, the spaces around the mine returns a value of 1.

This function forms the basis for Feature 2 to perform as expected.

The test function is as follows:

```python
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
```

## Implementation Plan (R7)

For the implementation plan of this project, the online project management tool Trello was used to draft up an outline of the plan for the overall project, as well as checklists for each individual feature. Labels were used to identify which features are the most important to complete first in order to have the game working, and which features can be implemented later or are optional. Due dates are also set for each task in the project in order to gauge the overall progress and time management.

See below for screenshots of the Trello board for this project, as well as the labels and checklists for each of the features:

![Trello Board](docs/trello_board.PNG)

![Trello Labels](docs/trello_labels.PNG)

![Trello Feature 1](docs/trello_feature1.PNG)

![Trello Feature 2](docs/trello_feature2.PNG)

![Trello Feature 3](docs/trello_feature3.PNG)

![Trello Feature 4](docs/trello_feature4.PNG)

![Trello Feature 5](docs/trello_feature5.PNG)

![Trello Feature 6](docs/trello_feature6.PNG)

## Installation Instructions (R8)

1. Open your terminal and create a new directory
2. Open this directory and enter the following command in terminal:

   ```git clone https://github.com/matthewngc/MatthewNg_T1A3```

3. Navigate into the folder by entering the following command:
   ```cd MatthewNg_T1A3```

4. Change the permissions on the script file by running the following command:

   ```chmod +x src/game.sh```

5. To run the terminal application, use the following command:

    ```./src/game.sh```

## System Dependencies & Requirements

There are no system dependencies or hardware requirements for this application.

This application will require Python to run. If you don't have Python installed, please visit <https://python.org/downloads/> to download the latest version.

## Style Guide (R5)

The python code for this project conforms to the standards set out in the PEP 8 Style Guide for Python.

## Referenced Sources (R3)

[PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)
