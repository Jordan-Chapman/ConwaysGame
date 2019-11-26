# By Jordan Chapman.
# Honestly I had to jury-rig this to get it to work, would have been much easier using a Game object,
# but the requirements specify "functions in a life_functions.py file"

import life_functions # DONE THIS WAY ON PURPOSE! Done to be able to edit global variables
import time
from os import system

# Variables
live = "*"
dead = "_"
default = False
width = 10
height = 10
freq = 33
delay = 500


choice = input("Are you using the pycharm console? ")

if choice.lower() in ["yes","y"]:
    default = True
    print("Using default settings")
else:
    print("Using cmd settings")
    live = "█"
    dead = " "
print("For larger sizes, you may want to use full screen.")

opt = input("Change settings? ")

if opt in ["yes", "y"]:
    try:
        width = int(input("Board width: "))
        height = int(input("Board height: "))
        freq = float(input("Population %: "))
        delay = int(input("Delay (in miliseconds): "))
        if freq < 1:
            freq = int(freq*100)
        else:
            freq = int(freq)
    except:
        input("Not understood, using default for the remainder of the settings.")


board = life_functions.load_board(width, height, freq) # Width, length, and population of the board.

while True:
    if default:
        print()
        life_functions.show_board(board, live, dead, grid=True, dupe=False)
    else:
        system("cls")
        life_functions.show_board(board, live, dead, grid=False, dupe=True)
    board = life_functions.operate_board(board)
    time.sleep(delay/1000)
