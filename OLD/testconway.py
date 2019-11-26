# A python example of conways game of life.
# Note that in board reading, the y coordinate goes before the x coordinate.
# This is caused by the way indexing works when arrays are inside arrays.

import random
import pygame
import time

class Game(object):
    sizex = 170  # Width
    sizey = 96  # Height
    population = 30  # As a percentage
    Scale = 8
    color = 250
    tick_delay = 0

    def __init__(self):
        self.board = []
        self.newboard = []
        self.changes = {}
        self.size = Game.sizex * Game.Scale, Game.sizey * Game.Scale
        self.current_time = time.time()

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
        while True:  # Mainloop
            self._wait_frame()
            self.operation()
            pygame.event.get()

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
        self.designs = self.load_cells("Patterns.txt")
        self.spawn_cells(self.designs[3],100,100)

    def _wait_frame(self):
        "Wait for the correct fps time to expire"
        pygame.time.delay(Game.tick_delay)

    def check_grid(self):
        nb_board = []
        for i in range(Game.sizey):
            nb_board.append(self.empty_row.copy())
        for y in range(Game.sizey):
            row = self.board[y]
            for x in range(Game.sizex):
                if row[x]: # Check if cell is live.
                    for X in [-1,0,1]:
                        for Y in [-1,0,1]:
                            if X or Y:
                                newx = x + X
                                newy = y + Y
                                try:
                                    nb_board[newy][newx] += 1
                                except:
                                    if newx > Game.sizex-1:
                                        newx -= Game.sizex
                                    if newy > Game.sizey-1:
                                        newy -= Game.sizey
                                    nb_board[newy][newx] += 1
        return nb_board

    def operation(self):
        self.newboard = self.check_grid()
        for y in range(Game.sizey):
            for x in range(Game.sizex):
                cell = self.newboard[y][x]
                current = self.board[y][x]
                if cell == 3 and not current:
                    self.board[y][x] = 1
                    # self.surface.set_at((x, y), Game.color)
                    pygame.draw.rect(self.surface, Game.color, (x * Game.Scale, y * Game.Scale, Game.Scale, Game.Scale),0)
                if cell not in [2,3] and current:
                    self.board[y][x] = 0
                    # self.surface.set_at((x, y), pygame.Color("black"))
                    pygame.draw.rect(self.surface, pygame.Color("black"),(x * Game.Scale, y * Game.Scale, Game.Scale, Game.Scale), 0)
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
