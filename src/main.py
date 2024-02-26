import pygame
import sys
from Pong.components import Ball, Arena, Paddle, Scorer
from Pong.gamelogic import GameLogic
from Pong.graphics import Animation

WIDTH = 800
HEIGHT = 600
FPS = 60

class App:
    def __init__(self):
        pygame.init()
        self.graphic = Animation(HEIGHT, WIDTH)

        #Create Game Components
        self.arena = Arena(WIDTH, HEIGHT)
        self.ball = Ball(WIDTH // 2, HEIGHT // 2)
        self.left_paddle = Paddle(self.arena.x, self.arena.height // 2 - Paddle.DEFAULT_HEIGHT // 2, self.arena)
        self.right_paddle = Paddle(self.arena.width + self.arena.x - Paddle.DEFAULT_WIDTH, self.arena.height // 2 - Paddle.DEFAULT_HEIGHT // 2, self.arena)
        self.scorer = Scorer()
        self.components = [self.arena, self.ball, self.left_paddle, self.right_paddle, self.scorer]

        #Create Game Trackers
        self.game_logic = GameLogic(self.ball, self.scorer, self.arena)
        self.clock = pygame.time.Clock()
        self.is_running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.VIDEORESIZE:
                self.resize(event.w, event.h)
                self.graphic.width = event.w
                self.graphic.height = event.h

    def resize(self, w, h):
        self.graphic.resize(w, h, self.components)

    def update(self):
        self.ball.update()
        self.left_paddle.update()
        self.right_paddle.update()
        self.arena.check_collision(self.ball, self.left_paddle, self.right_paddle)
        self.game_logic.update()

    def draw(self):
        self.graphic.draw(self.components)

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