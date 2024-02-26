import pygame

class Ball:
    def __init__(self, x, y):
        self.radius = 10
        self.x = x
        self.y = y
        self.vel_x = 5
        self.vel_y = 5
        self.tail_positions = []
        self.max_tails = 50

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
        self.vel = 7
        self.arena = arena

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.y - self.vel > self.arena.y:
            self.y -= self.vel
        if keys[pygame.K_DOWN] and self.y + self.vel < self.arena.y + self.arena.height - self.height:
            self.y += self.vel

    def resize(self, width_ratio, height_ratio):
        self.width *= width_ratio
        self.height *= height_ratio

        self.x *= width_ratio
        self.y *= height_ratio

        scaling_factor = (width_ratio + height_ratio) / 2
        self.vel *= scaling_factor
        

class Arena:
    def __init__(self, width, height):
        self.width = int(width * 0.8)
        self.height = int(height * 0.8)
        self.x = int(width * 0.1)
        self.y = int(height * 0.1)
        

    def check_collision(self, ball, left_paddle, right_paddle):
         # Check collision with top and bottom boundaries
        if ball.y <= self.y + ball.radius or ball.y >= self.y + self.height - ball.radius:
            ball.vel_y *= -1

        # Check collision with left paddle
        if (self.x + left_paddle.width + ball.radius > ball.x > self.x and left_paddle.y < ball.y < left_paddle.y + left_paddle.height):
            ball.vel_x *= -1

        # Check collision with right paddle
        if (self.x + self.width - right_paddle.width - ball.radius < ball.x < self.x + self.width and right_paddle.y < ball.y < right_paddle.y + right_paddle.height):
            ball.vel_x *= -1

    def resize(self, width_ratio, height_ratio):
        self.width *= width_ratio
        self.height *= height_ratio
        self.x *= width_ratio
        self.y *= height_ratio

class Scorer:
    def __init__(self, font_size=36):
        self.font = pygame.font.SysFont(None, font_size)
        self.score_left = 0
        self.score_right = 0

    def resize(self, width_ratio, height_ratio):
        pass