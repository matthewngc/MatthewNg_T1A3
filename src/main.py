"""Import modules"""
import os
import re
import time
from makeboard import createboard, display_board
from controls import show_space, place_flag
from prompts import press_to_continue, replay

# Play function
def play():
    """Function to play the game"""
    os.system("clear")
    print("Welcome to Minesweeper!")
    while True:
        difficulty = input("Please enter the difficulty you want to play on. \n"
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

    # Create a new board with random mines based on user input
    newboard = createboard(dimensions, max_mines)
    #print(newboard) #DEBUG
    start_time = time.time()
    emptyspace = True
    input_history = set()
    # Create a board that the player sees and updates when spaces are revealed
    player_board = [[' ' for i in range(dimensions)] for j in range(dimensions)]
    while len(input_history) < dimensions ** 2 - max_mines:
        os.system("clear")
        display_board(player_board)
        user_input = re.split(r"[-;,.\s]\s*", input("Please enter a coordinate (row,column). \nTo place a flag, type F after the coordinate (row,column,F) \n"))
        user_input = list(filter(None, user_input))
        if len(user_input) > 3:
            print("You've entered too many coordinates! Please try again.")
            press_to_continue()
            continue
        if len(user_input) < 2:
            print("You haven't entered enough coordinates! Please try again.")
            press_to_continue()
            continue
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
        if len(user_input) == 3:
            if flag.lower() == "f":
                place_flag(player_board,row, col)
                continue
            else:
                print("That is not a valid coordinate! To place a flag, type F after the coordinate (row,column,F).")
                press_to_continue()
                continue

        emptyspace = show_space(player_board, dimensions, newboard, row, col, input_history)
        if not emptyspace:
            break
    # Winning message when all empty spaces are revealed
    if emptyspace:
        os.system("clear")
        print("Congrats, you won!")
        display_board(newboard)
        print(f"Your time was {int(time.time()-start_time)} seconds!")
        if replay() is False:
            return
        else:
            play()

    # Losing message when a mine is revealed
    else:
        os.system("clear")
        print("You stepped on a mine! Game over!")
        display_board(newboard)
        if replay() is False:
            return
        else:
            play()


play()
