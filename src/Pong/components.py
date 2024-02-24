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
    def __init__(self, x, y):
        self.width = 20
        self.height = 120
        self.x = x
        self.y = y
        self.vel = 7

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.vel
        if keys[pygame.K_DOWN] and self.y < 600 - self.height:
            self.y += self.vel

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))  

class Arena:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def check_collision(self, ball, left_paddle, right_paddle):
        if ball.y <= ball.radius or ball.y >= self.y + self.height - ball.radius:
            ball.vel_y *= -1
        if ball.x <= left_paddle.x + left_paddle.width and left_paddle.y <= ball.y <= left_paddle.y + left_paddle.height:
            ball.vel_x *= -1
        if ball.x >= right_paddle.x - ball.radius and right_paddle.y <= ball.y <= right_paddle.y + right_paddle.height:
            ball.vel_x *= -1

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height), 2)