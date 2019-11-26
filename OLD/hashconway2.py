# Re-write of hashconway using a list for cell location instead of a dict.
# Hint - its slower :(
import random
import pygame
import time

class Game(object):
    sizex = 640  # Width
    sizey = 480  # Height
    population = sizex*sizey//3  # As a number
    scale = 1
    color = 250
    tick_delay = 0
    move_speed = 2

    def __init__(self):
        self.cells = []
        self.neighbors = {}
        self.size = Game.sizex * Game.scale, Game.sizey * Game.scale
        self.current_time = time.time()
        self.xdist = 0
        self.ydist = 0
        self.paused = False
        self.move_speed = Game.move_speed

    def end_fps(self):
        return time.time() - self.current_time

    def start_fps(self):
        self.current_time = time.time()

    def start(self):
        pygame.init()
        self.surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.load_cells()
        frames = 0
        self.start_fps()
        while True:  # Mainloop
            self.show_cells()
            pygame.display.set_caption((str(-self.xdist)+", "+str(self.ydist)))
            pygame.event.get()
            if pygame.key.get_pressed()[pygame.K_UP] == 1:
                self.ydist += self.move_speed
            if pygame.key.get_pressed()[pygame.K_DOWN] == 1:
                self.ydist -= self.move_speed
            if pygame.key.get_pressed()[pygame.K_LEFT] == 1:
                self.xdist += self.move_speed
            if pygame.key.get_pressed()[pygame.K_RIGHT] == 1:
                self.xdist -= self.move_speed
            if pygame.key.get_pressed()[pygame.K_RETURN] == 1:
                self.paused = True
            if pygame.key.get_pressed()[pygame.K_SPACE] == 1:
                self.paused = False
            if pygame.key.get_pressed()[pygame.K_RSHIFT] == 1 or pygame.key.get_pressed()[pygame.K_LSHIFT] == 1:
                self.move_speed = Game.move_speed * 2
            else:
                self.move_speed = Game.move_speed
            if not self.paused:
                self.operation()
            self._wait_frame()
            frames += 1
            if self.end_fps() > 1:
                print(frames)
                self.start_fps()
                frames = 0

    def gen_cells(self):
        # Generate board
        newcells = random.sample(range(Game.sizex*Game.sizey), Game.population)
        for cell in newcells:
            x = cell % Game.sizex
            y = cell // Game.sizex
            self.cells.append([x,y])

    def load_cells(self):
        self.designs = self.load_file("Patterns.txt")
        self.spawn_cells(self.designs[2],200,100)

    def _wait_frame(self):
        "Wait for the correct fps time to expire"
        pygame.time.delay(Game.tick_delay)

    def check_cells(self):
        new_neighbors = {}
        for cell in self.cells:
            for x in [-1,0,1]:
                for y in [-1,0,1]:
                    if x or y:
                        newcell = (cell[0]+x, cell[1]+y)
                        try:
                            new_neighbors[newcell] += 1
                        except:
                            new_neighbors[newcell] = 1
        return new_neighbors

    def operation(self):
        self.neighbors = self.check_cells()
        newcells = []
        for cell in self.neighbors.keys():
            nbcount = self.neighbors[cell]
            was_alive = [cell[0],cell[1]] in self.cells
            x = (cell[0] + self.xdist) * Game.scale
            y = (cell[1] + self.ydist) * Game.scale
            if nbcount == 3 or (nbcount == 2 and was_alive):
                newcells.append([cell[0],cell[1]])
        self.cells = newcells

    def show_cells(self):
        self.surface.fill((0,0,0))
        for cell in self.cells:
            x = (cell[0] + self.xdist) * Game.scale
            y = (cell[1] + self.ydist) * Game.scale
            if x >= 0 and y >= 0 and x < self.size[0] and y < self.size[1]:
                pygame.draw.rect(self.surface, Game.color, (x, y, Game.scale, Game.scale),0)
        pygame.display.flip()

    def load_file(self, filename):
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
            self.cells.append([x,y])

game = Game()
game.start()
