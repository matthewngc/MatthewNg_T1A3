"""Import os module"""
import os

# Press to continue function
def press_to_continue():
    """Press to continue function"""
    os.system("/bin/bash -c 'read -s -n 1 -p \"\nPress any key to continue.\"'\n")
    os.system('clear')

# Replay function prompts the user if they want to play again
def replay():
    """Prompts user and asks if they want to play again"""
    while True:
        play_again = input("Would you like to play again? (y/n) \n").lower()
        if play_again == "y":
            break
        elif play_again == "n":
            print("Thanks for playing!")
            return False
        else:
            print("Invalid input - please enter 'y' or 'n'.")
