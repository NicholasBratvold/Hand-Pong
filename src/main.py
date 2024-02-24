import pygame
import sys
from Pong.components import Ball, Arena, Paddle
from Pong.scorer import Scorer
from Pong.gamelogic import GameLogic

WIDTH = 800
HEIGHT = 600
FPS = 60

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        self.is_running = True
        
        self.arena = Arena(WIDTH, HEIGHT)
        self.ball = Ball(WIDTH // 2, HEIGHT // 2)
        self.left_paddle = Paddle(self.arena.x, self.arena.height // 2 - Paddle.DEFAULT_HEIGHT // 2, self.arena)
        self.right_paddle = Paddle(self.arena.width + self.arena.x - Paddle.DEFAULT_WIDTH, self.arena.height // 2 - Paddle.DEFAULT_HEIGHT // 2, self.arena)
        self.scorer = Scorer()
        self.game_logic = GameLogic(self.ball, self.scorer, self.arena)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def update(self):
        self.ball.update()
        self.left_paddle.update()
        self.right_paddle.update()
        self.arena.check_collision(self.ball, self.left_paddle, self.right_paddle)
        self.game_logic.update()

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.ball.draw(self.screen)
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.arena.draw(self.screen)
        self.scorer.draw(self.screen, WIDTH)
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