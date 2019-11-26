# Side/remake of hashconway, this time its "3d"
# Controls same, z to go down a layer, x to go up
import random
import pygame
import time

class Game(object):
    screen_x = 640 # Width of screen
    screen_y = 480 # Height of screen
    sizex = 10  # Spawnrange x
    sizey = 10  # Spawnrange y
    sizez = 10  # Spawnrange z
    scale = 8 # Block size

    population = sizex*sizey*sizez//5  # As a number
    life = (0,250,0) # Color of life
    death = (0,0,0) # Color of death
    tick_delay = 0 # Frame delay, needs to be phased out
    move_speed = 2 # Scroll speed using arrow keys, doubled while holding shift

    #Rules
    birth = [6,7]
    survive = [4,5]

    def __init__(self):
        self.cells = {}
        self.neighbors = {}
        self.size = Game.screen_x, Game.screen_y
        self.current_time = time.time()
        self.xdist = 0
        self.ydist = 0
        self.zdist = 0
        self.paused = True
        self.move_speed = Game.move_speed
        self.fps = 0

    def end_fps(self):
        return time.time() - self.current_time

    def start_fps(self):
        self.current_time = time.time()

    def start(self):
        pygame.init()
        self.surface = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.gen_cells()
        frames = 0
        self.start_fps()
        while True:  # Mainloop
            self.show_cells()
            pygame.display.set_caption((str(-self.xdist)+", "+str(self.ydist)+", "+str(self.zdist)+", FPS: "+str(self.fps)))
            pygame.event.get()
            if pygame.key.get_pressed()[pygame.K_UP] == 1:
                self.ydist += self.move_speed
            if pygame.key.get_pressed()[pygame.K_DOWN] == 1:
                self.ydist -= self.move_speed
            if pygame.key.get_pressed()[pygame.K_LEFT] == 1:
                self.xdist += self.move_speed
            if pygame.key.get_pressed()[pygame.K_RIGHT] == 1:
                self.xdist -= self.move_speed
            if pygame.key.get_pressed()[pygame.K_z] == 1:
                self.zdist += 1
            if pygame.key.get_pressed()[pygame.K_x] == 1:
                self.zdist -= 1
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
                self.fps = (frames/self.end_fps())
                self.start_fps()
                frames = 0
            print(len(self.cells))

    def gen_cells(self):
        # Generate board
        used = []
        x = None
        y = None
        z = None
        for i in range(Game.population):
            while True:
                x = random.randint(0, Game.sizex)
                y = random.randint(0, Game.sizey)
                z = random.randint(0, Game.sizez)
                if [x,y,z] not in used:
                    used.append([x,y,z])
                    break
            self.cells[(x,y,z)] = True

    def load_cells(self):
        self.designs = self.load_file("Patterns.txt")
        self.spawn_cells(self.designs[6],400,200)
        self.spawn_cells(self.designs[6],300,100, flip_x=True, rotate=True)
        self.spawn_cells(self.designs[6],200,200, flip_x=True)
        self.spawn_cells(self.designs[6],300,300, rotate=True)

    def _wait_frame(self):
        "Wait for the correct fps time to expire"
        pygame.time.delay(Game.tick_delay)

    def check_cells(self):
        new_neighbors = {}
        for cell in self.cells.keys():
            for x in [-1,0,1]:
                for y in [-1,0,1]:
                    for z in [-1,0,1]:
                        if x or y or z:
                            newcell = (cell[0]+x, cell[1]+y, cell[2]+z)
                            try:
                                new_neighbors[newcell] += 1
                            except:
                                new_neighbors[newcell] = 1
        return new_neighbors

    def operation(self):
        self.neighbors = self.check_cells()
        newcells = {}
        for cell in self.neighbors.keys():
            nbcount = self.neighbors[cell]
            was_alive = self.cells.get(cell)
            if nbcount in Game.birth or (nbcount in Game.survive and was_alive):
                newcells[cell] = True
        self.cells = newcells

    def show_cells(self):
        self.surface.fill(Game.death)
        for cell in self.cells.keys():
            x = (cell[0] + self.xdist) * Game.scale
            y = (cell[1] + self.ydist) * Game.scale
            z = cell[2] + self.zdist
            if x >= 0 and y >= 0 and x < self.size[0] and y < self.size[1] and z == 0:
                pygame.draw.rect(self.surface, Game.life, (x, y, Game.scale, Game.scale),0)
        pygame.display.flip()

    def load_file(self, filename):
        file = open(filename, "r")
        lines = file.readlines()
        file.close()
        return lines

    def spawn_cells(self, string, left, top, flip_x=False, flip_y=False, rotate=False):
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
                x,y = y,x
            x += left
            y += top
            self.cells[(x,y)] = True

game = Game()
game.start()
