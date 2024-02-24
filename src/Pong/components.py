import pygame


class Ball:
    def __init__(self, x, y):
        self.radius = 10
        self.x = x
        self.y = y
        self.vel_x = 5
        self.vel_y = 5

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius)

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

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))

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

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2)