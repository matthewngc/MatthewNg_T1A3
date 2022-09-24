import re

user_input = re.split(r"[-;,.\s]\s*", input("Please enter a coordinate (row,column).\n To place a flag, type F after the coordinate (row,column,F) \n"))
try:
    row, col, flag = int(user_input[0])-1, int(user_input[1])-1, user_input[-1]
except ValueError:
    print("Invalid")