import pygame
import numpy as np
from scipy.signal import convolve2d

class Ball:
    def __init__(self, x, y, radius=10, vel_x=5, vel_y=5):
        self.radius = radius
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.tail_positions = [(x, y)]
        self.max_tails = 20
        self.hit = False
        self.hit_time = 10

    def copy(self):
        return Ball(self.x, self.y, self.radius, self.vel_x, self.vel_y)

    def update(self, dt):
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt

        self.tail_positions.insert(0, (self.x, self.y))
        if len(self.tail_positions) > self.max_tails:
            self.tail_positions.pop()
        
        if self.hit:
            self.hit_time -= 1
            if self.hit_time <= 0:
                self.hit = False
                self.hit_time = 10

    def resize(self, width_ratio, height_ratio):
        self.x *= width_ratio
        self.y *= height_ratio

        scaling_factor = (width_ratio + height_ratio) / 2
        self.vel_x *= scaling_factor
        self.vel_y *= scaling_factor


class Paddle:
    DEFAULT_WIDTH = 20
    DEFAULT_HEIGHT = 120

    def __init__(self, x, y, arena, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.speed = 10
        self.vel = 0
        self.arena = arena
        self.hit = False

    def copy(self):
        arena = self.arena.copy()
        return Paddle(self.x, self.y, arena, self.width, self.height)

    def update(self, dt):
        self.y += self.vel * dt

    def resize(self, width_ratio, height_ratio):
        self.width *= width_ratio
        self.height *= height_ratio

        self.x *= width_ratio
        self.y *= height_ratio

        scaling_factor = (width_ratio + height_ratio) / 2
        self.vel *= scaling_factor
        

class Arena:

    UPDATE_RATE = 10
    GRID_SCALE = 4
    HEIGHT_RATIO = 0.6
    WIDTH_RATIO = 0.6

    def __init__(self, width, height):
        self.width = int(width * self.WIDTH_RATIO)
        self.height = int(height * self.HEIGHT_RATIO)
        self.x = int(width * ((1.0 - self.WIDTH_RATIO)/2))
        self.y = int(height * ((1.0 - self.HEIGHT_RATIO)/2))

        self.cols = int(self.width // self.GRID_SCALE)
        self.rows = int(self.height // self.GRID_SCALE)
        self.update_counter = 0
        self.cell_size = self.width // self.cols, self.height // self.rows
        self.grid = np.zeros((self.rows, self.cols))
        self.dirty_cells = []

        
    def copy(self):
        return Arena(self.width / Arena.WIDTH_RATIO, self.height / Arena.HEIGHT_RATIO)
    
    def update(self, dt):

        # print(f"Updated grid: {self.grid}")  # Add this line
        # print(f"Dirty cells: {self.dirty_cells}")  # Add this line

        self.update_counter += dt
        if self.update_counter >= self.UPDATE_RATE:
            self.update_counter = 0
            kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
            neighbors = convolve2d(self.grid, kernel, mode='same', boundary='fill', fillvalue=0)
            birth = (neighbors == 3) & (self.grid == 0)
            survive = ((neighbors == 2) | (neighbors == 3)) & (self.grid == 1)
            new_grid = birth | survive

             # Find the cells that have changed state
            changed_cells = np.where(new_grid != self.grid)

            # Update the dirty_cells list with the changed cells
            self.dirty_cells = list(zip(changed_cells[0], changed_cells[1]))

            # Update the grid
            self.grid = new_grid

    def resize(self, width_ratio, height_ratio):
        self.width =int(self.width * width_ratio)
        self.height = int(self.height * height_ratio)
        self.x = int(self.x * width_ratio)
        self.y = int(self.y * height_ratio)
        
        self.cols = int(self.width // self.GRID_SCALE)
        self.rows = int(self.height // self.GRID_SCALE)
        self.update_counter = 0
        self.cell_size = self.width // self.cols, self.height // self.rows
        self.grid = np.zeros((self.rows, self.cols))

class Scorer:
    def __init__(self, font_size=36):
        self.font = pygame.font.SysFont(None, font_size)
        self.score_left = 0
        self.score_right = 0

    def copy(self):
        return Scorer()

    def resize(self, width_ratio, height_ratio):
        pass

    def update(self, dt):
        pass