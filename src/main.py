import pygame
import sys

# Constants
WIDTH = 800
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60

# Components package
from Pong.components import Ball, Arena, Paddle

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.arena = Arena(50, 50, WIDTH - 100, HEIGHT - 100)
        self.ball = Ball(WIDTH // 2, HEIGHT // 2)
        self.left_paddle = Paddle(20, HEIGHT // 2 - 60)
        self.right_paddle = Paddle(WIDTH - 40, HEIGHT // 2 - 60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def update(self):
        self.ball.update()
        self.left_paddle.update()
        self.right_paddle.update()
        self.arena.check_collision(self.ball, self.left_paddle, self.right_paddle)

    def draw(self):
        self.screen.fill(BLACK)
        self.ball.draw(self.screen)
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.arena.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = App()
    app.run()