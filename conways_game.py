# A re-write of my original conways game.
# This one uses a dictionary to store coordinates, and does away with grids entirely.
# May be slower, but grid is infinite.
# Controls: Enter to pause, Space to resume, arrow keys to move, hold shift to move faster.

import random
import pygame
import time
import math


class Game(object):
    """
    The game object
    """
    screen_x = 640  # Width of screen
    screen_y = 480  # Height of screen
    sizex = 50  # Spawnrange x (square radius)
    sizey = 50  # Spawnrange y (square radius)
    deathx = 0  # Radius at which cell spontaniously combust
    deathy = 0  # ^

    scale = 8  # Starting block size
    max_scale = 1000  # Max pixel size of a cell by scaling.
    min_scale = 1  # Min pixel size of a cell by scaling.
    scale_speed = 1.01  # Multiplied/divided by Game.scale to scale the board. Higher values scale faster
    scale_snap = 100  # Higher scale_snap increases smoothness of scaling farther out, but also increases amount of grid_like scales. 1 is perfect snap, 0 will crash

    population = sizex * sizey * 4 // 2  # As a number
    life = (0, 250, 0)  # Color of life
    death = (0, 0, 0)  # Color of death
    tick_delay = 0  # Frame delay, needs to be phased out
    move_speed = 3  # Scroll speed using arrow keys, doubled while holding shift

    # Rules
    birth = [3]
    survive = [2]

    def __init__(self):
        """
        Constructor
        """
        self.cells = {}
        self.neighbors = {}
        self.size = Game.screen_x, Game.screen_y
        self.counters = {}
        self.xdist = 0
        self.ydist = 0
        self.paused = True
        self.move_speed = Game.move_speed
        self.fps = 0
        self.pressed_keys = []

    def start_fps(self, name):
        """
        Start counting frames
        :param name: Name of counter to start
        :return: None
        """
        self.counters[name] = time.time()

    def end_fps(self, name):
        """
        Check the frame counter started in start_fps
        :param name: Name of counter to check
        :return: # of frames since start_fps was called
        """
        return time.time() - self.counters[name]

    def handle_events(self):
        """
        Handle keyboard events
        :return: None
        """
        # self.split("test")
        pygame.display.set_caption(
            (str(int(-self.xdist)) + ", " + str(int(self.ydist)) + ", FPS: " + str(int(self.fps))))
        pygame.event.get()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] == 1 or keys[pygame.K_w] == 1:
            self.ydist += self.move_speed / Game.scale

        if keys[pygame.K_DOWN] == 1 or keys[pygame.K_s] == 1:
            self.ydist -= self.move_speed / Game.scale

        if keys[pygame.K_LEFT] == 1 or keys[pygame.K_a] == 1:
            self.xdist += self.move_speed / Game.scale

        if keys[pygame.K_RIGHT] == 1 or keys[pygame.K_d] == 1:
            self.xdist -= self.move_speed / Game.scale

        if keys[pygame.K_RETURN] == 1:
            if pygame.K_RETURN not in self.pressed_keys:
                self.paused = not self.paused
                self.pressed_keys.append(pygame.K_RETURN)
        elif pygame.K_RETURN in self.pressed_keys:
            self.pressed_keys.remove(pygame.K_RETURN)

        if keys[pygame.K_z] == 1:
            if Game.scale >= Game.max_scale:
                Game.scale = Game.max_scale
            else:
                Game.scale *= Game.scale_speed

        if keys[pygame.K_x] == 1:
            if Game.scale <= Game.min_scale:
                Game.scale = Game.min_scale
            else:
                Game.scale /= Game.scale_speed

        if keys[pygame.K_c] == 1:
            Game.scale = int(Game.scale)

        if keys[pygame.K_RSHIFT] == 1 or pygame.key.get_pressed()[pygame.K_LSHIFT] == 1:
            self.move_speed = Game.move_speed * 2
        else:
            self.move_speed = Game.move_speed

        if pygame.mouse.get_pressed()[0]:
            x, y = pygame.mouse.get_pos()
            x = x - (Game.screen_x / 2)
            y = y - (Game.screen_y / 2)
            x = round(x / Game.scale - self.xdist - 0.5)
            y = round(y / Game.scale - self.ydist - 0.5)
            self.cells[(x, y)] = True

        if pygame.mouse.get_pressed()[2]:
            x, y = pygame.mouse.get_pos()
            x = x - (Game.screen_x / 2)
            y = y - (Game.screen_y / 2)
            x = round(x / Game.scale - self.xdist - 0.5)
            y = round(y / Game.scale - self.ydist - 0.5)
            try:
                self.cells.pop((x, y))
            except:
                pass

        # print("Handle events: ",self.show("test"))

    def start(self):
        """
        Start the program
        :return: None
        """
        pygame.init()
        self.surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.gen_cells()
        frames = 0
        self.start_fps("main")
        while True:  # Mainloop
            # self.split("test")
            self.show_cells()
            # print("Update display: ",self.show("test"))
            self.handle_events()
            if not self.paused:
                neighbors = self.check_cells()
                self.cells = self.operation(neighbors)
            # self.split("test")
            self._wait_frame()
            frames += 1
            if self.end_fps("main") > 1:
                self.fps = (frames / self.end_fps("main"))
                self.start_fps("main")
                frames = 0
            # print("Frame handling: ",self.show("test"))

    def gen_cells(self):
        """
        Generate cells at random
        :return: None
        """
        # Generate board
        newcells = random.sample(range(Game.sizex * Game.sizey * 4), Game.population)
        for cell in newcells:
            x = cell % (Game.sizex * 2) - Game.sizex
            y = cell // (Game.sizex * 2) - Game.sizex
            self.cells[(x, y)] = True

    def load_cells(self):
        """
        Load cells from a file
        :return: None
        """
        self.designs = self.load_file("Patterns.txt")
        # self.spawn_cells(self.designs[6],100,0)
        # self.spawn_cells(self.designs[6],0,-100, flip_x=True, rotate=True)
        # self.spawn_cells(self.designs[6],-100,0, flip_x=True)
        # self.spawn_cells(self.designs[6],0,100, rotate=True)
        self.spawn_cells(self.designs[2], 0, 0)

    def _wait_frame(self):
        """
        Delay the program by Game.tick_delay
        :return: None
        """
        "Wait for the correct fps time to expire"
        pygame.time.delay(Game.tick_delay)

    def check_cells(self):
        """
        Check for cell neighbors and kill out-of-range cells
        :return: Dictionary of cell coordinates and their neighbors
        """
        new_neighbors = {}
        marked_for_death = []
        for cell in self.cells.keys():
            if abs(cell[0]) > Game.deathx and Game.deathx or abs(cell[1]) > Game.deathy and Game.deathy:
                marked_for_death.append(cell)
            else:
                for x in [-1, 0, 1]:
                    for y in [-1, 0, 1]:
                        if x or y:
                            newcell = (cell[0] + x, cell[1] + y)
                            try:
                                new_neighbors[newcell] += 1
                            except:
                                new_neighbors[newcell] = 1
        for cell in marked_for_death:
            self.cells.pop(cell)
        return new_neighbors

    def operation(self, neighbors):
        """
        Operate on cells; Kill underpopulated, birth in right conditions
        :param neighbors: Neighbor dictionary to operate on
        :return: Dictionary of new cells
        """
        # self.split("test")
        # print("Neighbor finding: ",self.show("test"))
        # self.split("test")
        newcells = {}
        for cell in neighbors.keys():
            nbcount = neighbors[cell]
            was_alive = self.cells.get(cell)
            if nbcount in Game.birth or (nbcount in Game.survive and was_alive):
                newcells[cell] = True
        return newcells
        # print("Operation: ",self.show("test"))

    def show_cells(self):
        """
        Display new cells to the pygame window
        :return: None
        """
        self.surface.fill(Game.death)
        scale = int(Game.scale * Game.scale_snap) / Game.scale_snap
        for cell in self.cells.keys():
            x = int(((cell[0] + self.xdist) * scale) + Game.screen_x / 2)
            y = int(((cell[1] + self.ydist) * scale) + Game.screen_y / 2)
            if x + scale >= 0 and y + scale >= 0 and x < self.size[0] and y < self.size[1]:
                pygame.draw.rect(self.surface, Game.life, (x, y, int(math.ceil(scale)), int(math.ceil(scale))), 0)
        pygame.display.flip()

    def load_file(self, filename):
        """
        Load a text file
        :param filename:
        :return: List of each line of the text file
        """
        file = open(filename, "r")
        lines = file.readlines()
        file.close()
        return lines

    def spawn_cells(self, string, left, top, flip_x=False, flip_y=False, rotate=False):
        """
        Spawn cells to the board
        :param string: Coordinates of each cell in form 'x,y x,y x,y'
        :param left: Distance away from origin on the x axis
        :param top: Distance away from origin on the y axis
        :param flip_x: Whether to flip cells on the x axis
        :param flip_y: Whether to flip cells on the y axis
        :param rotate: Whether to rotate cells by 90 degrees
        :return: None
        """
        ls = string.split()
        cells = []
        for pair in ls:
            cells.append(pair.split(","))
        for cell in cells:
            x = int(cell[0])
            y = int(cell[1])
            if flip_x:
                x = -x
            if flip_y:
                y = -y
            if rotate:
                x, y = y, x
            x += left
            y += top
            self.cells[(x, y)] = True


game = Game()
game.start()
