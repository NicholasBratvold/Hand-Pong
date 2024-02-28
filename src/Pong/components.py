import pygame
import numpy as np

class Ball:
    def __init__(self, x, y, radius=10, vel_x=5, vel_y=5):
        self.radius = radius
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.tail_positions = []
        self.max_tails = 20

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y

        self.tail_positions.insert(0, (self.x, self.y))
        if len(self.tail_positions) > self.max_tails:
            self.tail_positions.pop()

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
        self.speed = 7
        self.vel = 0
        self.arena = arena

    def update(self):
        self.y += self.vel

    def resize(self, width_ratio, height_ratio):
        self.width *= width_ratio
        self.height *= height_ratio

        self.x *= width_ratio
        self.y *= height_ratio

        scaling_factor = (width_ratio + height_ratio) / 2
        self.vel *= scaling_factor
        

class Arena:

    UPDATE_RATE = 10
    GRID_SCALE = 5

    def __init__(self, width, height):
        self.width = int(width * 0.8)
        self.height = int(height * 0.8)
        self.x = int(width * 0.1)
        self.y = int(height * 0.1)

        self.cols = int(self.width // self.GRID_SCALE)
        self.rows = int(self.height // self.GRID_SCALE)
        self.update_counter = 0
        self.cell_size = self.width // self.cols, self.height // self.rows
        self.grid = np.zeros((self.rows, self.cols))
        
    
    def update(self):
        self.update_counter += 1
        if self.update_counter == self.UPDATE_RATE:
            self.update_counter = 0
            new_grid = np.copy(self.grid)
            for i in range(self.rows):
                for j in range(self.cols):
                    neighbors = self.get_neighbors(i, j)
                    if self.grid[i][j] == 1 and (neighbors < 2 or neighbors > 3):
                        new_grid[i][j] = 0
                    elif self.grid[i][j] == 0 and neighbors == 3:
                        new_grid[i][j] = 1
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

    def get_neighbors(self, x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if 0 <= x + i < self.rows and 0 <= y + j < self.cols:
                    count += self.grid[x + i][y + j]
        return count

class Scorer:
    def __init__(self, font_size=36):
        self.font = pygame.font.SysFont(None, font_size)
        self.score_left = 0
        self.score_right = 0

    def resize(self, width_ratio, height_ratio):
        pass

    def update(self):
        pass