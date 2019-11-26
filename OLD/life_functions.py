# By Jordan Chapman

import random


def generate_board(width, height, frequency):
    """
    Generates a board of 0s and 1s at %frequency
    :param width: The width of the board to generate
    :param height: The height of the board to generate
    :param frequency: The % of the board to be 1s
    :return: A populated board as a list of lists of characters.
    """
    board = []
    for y in range(height):
        board.append([])
        for x in range(width):
            char = 0
            chance = random.randint(1, 100)
            if chance < frequency:
                char = 1
            board[y].append(char)
    return board


def load_board(width, height, frequency):
    """
    Generates a board of 0s and 1s at %frequency
    :param width: The width of the board to generate
    :param height: The height of the board to generate
    :param frequency: The % of the board to be 1s
    :return: A populated board as a list of lists of characters.
    """
    board = []
    for i in range(height):
        board.append([0]*width)
    board[0][1] = 1
    board[1][2] = 1
    board[2][0] = 1
    board[2][1] = 1
    board[2][2] = 1

    board[10][0] = 1
    board[10][1] = 1
    board[10][2] = 1
    board[10][3] = 1
    board[11][0] = 1
    board[12][0] = 1
    board[13][1] = 1
    board[11][4] = 1
    board[13][4] = 1

    return board


def show_board(board, live, dead, grid=True, dupe=True):
    """
    Display a board in an aesthetically pleasing way
    :param board:
    :return: None
    """
    width = len(board[0])
    print((" " + dead) * width)
    for row in board:
        if grid:
            print("|", end="")
        else:
            print(" ", end="")
        for item in row:
            char = ""
            if item == 0:
                char = dead
            else:
                char = live
            if dupe:
                print(char*2, end="")
            else:
                print(char, end="|")
        print()


# def get_neighbors(board, x, y): # Old get_neighbors that doesnt wrap around the screen
#     """
#     Gets the amount of neighboring *s in a given board, for a given coordinate
#     :param board: Board to use
#     :param x: X coordinate
#     :param y: Y coordinate
#     :return: The number of * neighbors
#     """
#     directions = []  # This is a headache. This list contains all the coordinate directions to search for *s
#     if y > 0:
#         directions.append([-1, 0])  # Add y-1
#         if x > 0:
#             directions.append([-1, -1])  # Add y-1 x-1
#         if x < len(board[y]) - 1:
#             directions.append([-1, 1])  # Add y-1 x+1
#     if y < len(board) - 1:
#         directions.append([1, 0])  # Add y+1
#         if x > 0:
#             directions.append([1, -1])  # Add y+1 x-1
#         if x < len(board[y]) - 1:
#             directions.append([1, 1])  # Add y+1 x+1
#     if x > 0:
#         directions.append([0, -1])  # Add x-1
#     if x < len(board[y]) - 1:
#         directions.append([0, 1])  # Add x+1
#     neighbors = 0
#     for d in directions:  # Check for each added direction
#         try:
#             if board[y + d[0]][x + d[1]] == 1:
#                 neighbors += 1
#         except:
#             print(y, x, d)
#     return neighbors


def get_neighbors(board, x, y): # New get_neighbors that wraps around the screen
    """
    Gets the amount of neighboring *s in a given board, for a given coordinate
    :param board: Board to use
    :param x: X coordinate
    :param y: Y coordinate
    :return: The number of * neighbors
    """
    directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
    neighbors = 0
    for d in directions:
        new_y = y + d[0]
        new_x = x + d[1]
        if new_x >= len(board[y]):
            new_x -= len(board[y])
        if new_y >= len(board):
            new_y -= len(board)
        if new_x < 0:
            new_x += len(board[y])
        if new_y < 0:
            new_y += len(board)

        if board[new_y][new_x] == 1: # Increment counter
            neighbors += 1
    return neighbors


def operate_board(board):
    """
    Do the main operation on a given board
    :param board: Board to operate on
    :return: New board
    """
    newboard = []
    x = 0
    y = 0
    char = 0
    for y in range(len(board)):  # Y coordinates for each row of the board, with y=0 being the top row
        newboard.append([])
        for x in range(len(board[y])):  # Same goes for x coordinates, x=0 is far left
            neighbors = get_neighbors(board, x, y)
            if neighbors > 3 or neighbors < 2:  # Regardless of whether its alive, too many/few neighbors = dead cell
                char = 0
            elif neighbors == 3:  # Regardless of whether its alive, 3 neighbors = living cell
                char = 1
            else:
                char = board[y][x]  # 2 Neighbors means cell stays the same
            newboard[y].append(char)  # Add character to the new board, at row y
    return newboard
