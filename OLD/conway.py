# A python example of conways game of life.
# Note that in board reading, the y coordinate goes before the x coordinate.
# This is caused by the way indexing works when arrays are inside arrays.

import random
import pygame
import time

class Game(object):
    Sleep = True
    sleeptime = 0.1
    sizex = 400 # Width
    sizey = 250 # Height
    population = 30 # As a percentage
    Scale = 2
    color = 250
    tick_delay = 0
    spawnrate = 100 # As a percentage
    Spawntimer = 10
    def __init__(self):
        self.board = []
        self.size = Game.sizex*Game.Scale,Game.sizey*Game.Scale
        self.spawntimer = Game.Spawntimer
    def start(self):
        pygame.init()
        self.surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.generate_board()
        while True: # Mainloop
            self._wait_frame()
            self.operation()
            self.spawntimer -= 1
            if self.spawntimer <= 0:
                self.spawntimer = Game.Spawntimer
                self.spawn_new()
    def _wait_frame (self): 
        "Wait for the correct fps time to expire"
        pygame.time.delay(Game.tick_delay)
    def generate_board(self):
        # Generate board
        board = []
        for y in range(Game.sizey):
            newrow = ""
            for x in range(Game.sizex):
                if random.randint(1, 100) <= Game.population:
                    newrow += "0"
                    pygame.draw.rect(self.surface,Game.color,(x*Game.Scale,y*Game.Scale,Game.Scale, Game.Scale),0)
                else:
                    newrow += "-"
            board.append(newrow)
        self.board = board
    def spawn_new(self):
        for current in range(len(self.board)):
            if random.randint(1,100) < Game.spawnrate:
                selected = self.board[current]
                row = "00" + selected[2:]
                self.board[current] = selected
    def operation(self):
        # Board level
        self.surface.fill((0,0,0))
        newboard = []
        board = self.board
        pop = 0
        for y in range(Game.sizey):
            # Row level
            newrow = ""
            for x in range(Game.sizex):
                # Cell level
                near = 0
                if y > 0: # row above cell
                    if x > 0: # Topleft
                        if board[y-1][x-1] == "0":
                            near += 1
                    if board[y-1][x] == "0": # Top
                        near += 1
                    if x < Game.sizex-1: # Topright
                        if board[y-1][x+1] == "0":
                            near += 1
                if x > 0: # Left
                    if board[y][x-1] == "0":
                        near += 1
                if x < Game.sizex-1: # Right
                    if board[y][x+1] == "0":
                        near += 1
                if y < Game.sizey-1: # row below cell
                    if x > 0: # Bottomleft
                        if board[y+1][x-1] == "0":
                            near += 1
                    if board[y+1][x] == "0": # Bottom
                        near += 1
                    if x < Game.sizex-1: # Bottomright
                        if board[y+1][x+1] == "0":
                            near += 1
                if near < 2: # Underpopulation
                    newrow += "-"
                elif near > 3: # Overpopulation
                    newrow += "-"
                else: # Survivable population
                    if board[y][x] == "0" or near == 3: # Living, or reproduceable
                        newrow += "0"
                        pop += 1
                        pygame.draw.rect(self.surface,Game.color,(x*Game.Scale,y*Game.Scale,Game.Scale, Game.Scale),0)
                    else: # Non living, non reproduceable
                        newrow += "-"
            newboard.append(newrow)
##        print("\n".join(newboard))
##        time.sleep(Game.sleeptime)
        self.board = newboard
        pygame.display.flip()
game = Game()
game.start()
