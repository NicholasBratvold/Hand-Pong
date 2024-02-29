import pygame
import numpy as np
from scipy.signal import convolve2d


class Component:
    """
    Represents a component in the Pong game.

    A component is an element that appears in the game and can be updated and resized.

    Methods:
    - copy(): Creates a copy of the component object.
    - resize(width_ratio, height_ratio): Resizes the component based on the given width and height ratios.
    - update(dt): Updates the component based on the given time step.
    """

    def __init__(self):
        pass

    def copy(self):
        pass

    def resize(self, width_ratio, height_ratio):
        pass

    def update(self, dt):
        pass


class Ball(Component):
    """
    Represents a ball in the Pong game.

    Attributes:
    - radius: The radius of the ball.
    - x: The x-coordinate of the ball's position.
    - y: The y-coordinate of the ball's position.
    - vel_x: The velocity of the ball in the x-direction.
    - vel_y: The velocity of the ball in the y-direction.
    - tail_positions: A list of previous positions of the ball.
    - max_tails: The maximum number of tail positions to keep.
    - hit: A flag indicating if the ball has been hit.
    - hit_time: The remaining time for the hit effect.

    Methods:
    - copy(): Creates a copy of the ball object.
    - update(dt): Updates the ball's position and tail positions.
    - resize(width_ratio, height_ratio): Resizes the ball based on the given width and height ratios.
    """

    def __init__(self, x, y, radius=10, vel_x=5, vel_y=5):
        self.radius = radius
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.tail_positions = [(x, y)]
        self.max_tails = 20
        self.hit = False
        self.hit_time = 5

    def copy(self):
        """
        Creates a copy of the ball object.

        Returns:
        - A new Ball object with the same attributes as the original ball.
        """
        return Ball(self.x, self.y, self.radius, self.vel_x, self.vel_y)

    def update(self, dt):
        """
        Updates the ball's position and tail positions based on the given time step.

        Parameters:
        - dt: The time step for the update.
        """
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
        """
        Resizes the ball based on the given width and height ratios.

        Parameters:
        - width_ratio: The ratio to resize the ball's width.
        - height_ratio: The ratio to resize the ball's height.
        """
        self.x *= width_ratio
        self.y *= height_ratio

        scaling_factor = (width_ratio + height_ratio) / 2
        self.vel_x *= scaling_factor
        self.vel_y *= scaling_factor
        self.radius *= scaling_factor


class Paddle(Component):
    """
    Represents a paddle in the Pong game.

    Attributes:
    - DEFAULT_WIDTH: The default width of the paddle.
    - DEFAULT_HEIGHT: The default height of the paddle.
    - width: The width of the paddle.
    - height: The height of the paddle.
    - x: The x-coordinate of the paddle's position.
    - y: The y-coordinate of the paddle's position.
    - speed: The speed of the paddle.
    - vel: The velocity of the paddle.
    - arena: The arena in which the paddle is located.
    - hit: A flag indicating if the paddle has been hit.
    - hit_time: The remaining time for the hit effect.
    - left: A flag indicating if the paddle is on the left side of the arena.

    Methods:
    - copy(): Creates a copy of the paddle object.
    - update(dt): Updates the paddle's position.
    - resize(width_ratio, height_ratio): Resizes the paddle based on the given width and height ratios.
    """

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
        self.hit_time = 5
        self.left = x < arena.x + arena.width / 2

    def copy(self):
        """
        Creates a copy of the paddle object.

        Returns:
        - A new Paddle object with the same attributes as the original paddle.
        """
        arena = self.arena.copy()
        return Paddle(self.x, self.y, arena, self.width, self.height)

    def update(self, dt):
        """
        Updates the paddle's position.

        Parameters:
        - dt: The time step for the update.
        """
        self.y += self.vel * dt

        if self.hit:
            self.hit_time -= 1
            if self.hit_time <= 0:
                self.hit = False
                self.hit_time = 5

    def resize(self, width_ratio, height_ratio):
        """
        Resizes the paddle based on the given width and height ratios.

        Parameters:
        - width_ratio: The ratio to resize the paddle's width.
        - height_ratio: The ratio to resize the paddle's height.
        """
        self.width *= width_ratio
        self.height *= height_ratio

        self.x *= width_ratio
        self.y *= height_ratio

        scaling_factor = (width_ratio + height_ratio) / 2
        self.vel *= scaling_factor
        self.speed *= scaling_factor


class Arena(Component):
    """
    Represents the game arena in the Pong game.

    Attributes:
    - UPDATE_RATE: The update rate of the arena.
    - GRID_SCALE: The scale of the grid in the arena.
    - HEIGHT_RATIO: The height ratio of the arena to the game window.
    - WIDTH_RATIO: The width ratio of the arena to the game window.
    - width: The width of the arena.
    - height: The height of the arena.
    - x: The x-coordinate of the arena's position.
    - y: The y-coordinate of the arena's position.
    - cols: The number of columns in the arena's grid.
    - rows: The number of rows in the arena's grid.
    - update_counter: The counter for updating the arena.
    - cell_size: The size of each cell in the arena's grid.
    - grid: The grid representing the state of the arena.
    - dirty_cells: A list of cells that have changed state.

    Methods:
    - copy(): Creates a copy of the arena object.
    - update(dt): Updates the arena's state.
    - resize(width_ratio, height_ratio): Resizes the arena based on the given width and height ratios.
    """

    UPDATE_RATE = 10
    GRID_SCALE = 4
    HEIGHT_RATIO = 0.6
    WIDTH_RATIO = 0.6

    def __init__(self, width, height):
        # center the arena in the window
        self.width = int(width * self.WIDTH_RATIO)
        self.height = int(height * self.HEIGHT_RATIO)
        self.x = int(width * ((1.0 - self.WIDTH_RATIO) / 2))
        self.y = int(height * ((1.0 - self.HEIGHT_RATIO) / 2))

        # initialize the Conway's Game of Life grid
        self.cols = int(self.width // self.GRID_SCALE)
        self.rows = int(self.height // self.GRID_SCALE)
        self.update_counter = 0
        self.cell_size = self.width // self.cols, self.height // self.rows
        self.grid = np.zeros((self.rows, self.cols))
        self.dirty_cells = []

    def copy(self):
        """
        Creates a copy of the arena object.

        Returns:
        - A new Arena object with the same attributes as the original arena.
        """
        return Arena(self.width / Arena.WIDTH_RATIO, self.height / Arena.HEIGHT_RATIO)

    def update(self, dt):
        """
        Updates the arena's state.

        Parameters:
        - dt: The time step for the update.
        """

        self.update_counter += dt
        if self.update_counter >= self.UPDATE_RATE:
            self.update_counter = 0
            # convolving with this kernel gives count of cells around the center.
            kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
            neighbors = convolve2d(
                self.grid, kernel, mode="same", boundary="fill", fillvalue=0
            )

            # Apply the rules of Conway's Game of Life
            birth = (neighbors == 3) & (self.grid == 0)
            survive = ((neighbors == 2) | (neighbors == 3)) & (self.grid == 1)
            new_grid = birth | survive

            # Find the cells that have changed state
            changed_cells = np.where(new_grid != self.grid)

            self.dirty_cells = list(zip(changed_cells[0], changed_cells[1]))

            self.grid = new_grid

    def resize(self, width_ratio, height_ratio):
        """
        Resizes the arena based on the given width and height ratios.

        Parameters:
        - width_ratio: The ratio to resize the arena's width.
        - height_ratio: The ratio to resize the arena's height.
        """
        self.width *= width_ratio
        self.height *= height_ratio
        self.x *= width_ratio
        self.y *= height_ratio
        self.cols = int(self.width // self.GRID_SCALE)
        self.rows = int(self.height // self.GRID_SCALE)
        self.cell_size = self.width // self.cols, self.height // self.rows
        self.grid = np.zeros((self.rows, self.cols))
        self.dirty_cells = []


class Scorer(Component):
    """
    Represents the scorer in the Pong game.

    Attributes:
    - font: The font used for displaying the score.
    - score_left: The score of the left player.
    - score_right: The score of the right player.

    Methods:
    - copy(): Creates a copy of the scorer object.
    - resize(width_ratio, height_ratio): Resizes the scorer based on the given width and height ratios.
    - update(dt): Updates the scorer.

    """

    def __init__(self, font_size=36):
        self.font = pygame.font.SysFont(None, font_size)
        self.score_left = 0
        self.score_right = 0

    def copy(self):
        """
        Creates a copy of the scorer object.

        Returns:
        - A new Scorer object with scores set to 0.
        """
        return Scorer()

    def resize(self, width_ratio, height_ratio):
        """
        Does nothing for the scorer.
        """
        pass

    def update(self, dt):
        """
        Does nothing for the scorer.
        """
        pass
