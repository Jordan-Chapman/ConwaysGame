# A python example of conways game of life.
# Note that in board reading, the y coordinate goes before the x coordinate.
# This is caused by the way indexing works when arrays are inside arrays.

import random
import pygame
import time


class Cell(object):
    def __init__(self, game):
        self.game = game

    def check_neighbors(self):
        pass


class Game(object):
    sizex = 300  # Width
    sizey = 200  # Height
    population = 30  # As a percentage
    Scale = 1
    color = 250
    tick_delay = 0
    directions = [[-1, -1], [0, -1], [1, -1],
                  [-1,  0], [0,  0], [1,  0],
                  [-1,  1], [0,  1], [1,  1]]

    def __init__(self):
        self.board = []
        self.newboard = []
        self.size = Game.sizex * Game.Scale, Game.sizey * Game.Scale

    def end_fps(self):
        print(time.time() - self.current_time)
    def start_fps(self):
        self.current_time = time.time()

    def start(self):
        pygame.init()
        self.surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.generate_board()
        self.newboard = []
        self.empty_row = [0] * Game.sizex
        self.designs = self.load_cells("Patterns.txt")
        while True:  # Mainloop
            self.start_fps()
            self._wait_frame()
            self.operation()
            self.end_fps()
            print()

    def generate_board(self):
        # Generate board
        board = []
        for y in range(Game.sizey):
            newrow = []
            for x in range(Game.sizex):
                if random.randint(1, 100) <= Game.population:
                    newrow.append(1)
                    pygame.draw.rect(self.surface, Game.color, (x * Game.Scale, y * Game.Scale, Game.Scale, Game.Scale),
                                     0)
                else:
                    newrow.append(0)
            board.append(newrow)
        self.board = board
    def generate_empty(self):
        board = []
        for y in range(Game.sizey):
            newrow = []
            for x in range(Game.sizex):
                newrow.append(0)
            board.append(newrow)
        self.board = board

    def _wait_frame(self):
        "Wait for the correct fps time to expire"
        pygame.time.delay(Game.tick_delay)

    def check_grid(self):
        checks = 0
        nb_board = []
        for i in range(Game.sizey):
            nb_board.append(self.empty_row.copy())
        for y in range(Game.sizey):
            row = self.board[y]
            for x in range(Game.sizex):
                if row[x]: # Check if cell is live.
                    for direct in Game.directions:
                        checks += 1
                        newx = x + direct[0]
                        newy = y + direct[1]
                        try:
                            nb_board[newy][newx] += 1
                        except:
                            if newx > Game.sizex-1:
                                newx -= Game.sizex
                            if newy > Game.sizey-1:
                                newy -= Game.sizey
                            nb_board[newy][newx] += 1
        # print(checks)
        return nb_board

    def operation(self):
        self.newboard = self.check_grid()
        for y in range(Game.sizey):
            for x in range(Game.sizex):
                current = self.board[y][x]
                cell = self.newboard[y][x]
                if cell-current == 3:
                    self.board[y][x] = 1
                    if not current:
                        # self.surface.set_at((x, y), Game.color)
                        pygame.draw.rect(self.surface, Game.color, (x * Game.Scale, y * Game.Scale, Game.Scale, Game.Scale),0)
                elif cell-current == 2:
                    pass
                else:
                    self.board[y][x] = 0
                    if current:
                        # self.surface.set_at((x, y), pygame.Color("black"))
                        pygame.draw.rect(self.surface, pygame.Color("black"),
                                         (x * Game.Scale, y * Game.Scale, Game.Scale, Game.Scale), 0)
        pygame.display.flip()

    def load_cells(self, filename):
        file = open(filename, "r")
        lines = file.readlines()
        file.close()
        return lines

    def spawn_cells(self, string, top, left):
        ls = string.split()
        cells = []
        for pair in ls:
            cells.append(pair.split(","))
        for cell in cells:
            x = int(cell[0]) + left
            y = int(cell[1]) + top
            self.board[y][x] = 1
            pygame.draw.rect(self.surface, Game.color, (x * Game.Scale, y * Game.Scale, Game.Scale, Game.Scale), 0)


game = Game()
game.start()
