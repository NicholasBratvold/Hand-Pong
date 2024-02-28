import pygame
import sys
from Pong.components import Ball, Arena, Paddle, Scorer
from Pong.gamelogic import Game, StateManager, Menu
from Pong.graphics import Animation


WIDTH = 800
HEIGHT = 600
FPS = 60

#Game States
ONE_PLAYER = 1
TWO_PLAYER = 2
MENU = 0
QUIT = 4



class App:
    def __init__(self):
        pygame.init()
        
        #Create Game Components
        self.arena = Arena(WIDTH, HEIGHT)
        self.ball1 = Ball(WIDTH // 2, HEIGHT // 2)
        self.ball2 = Ball(WIDTH // 2, HEIGHT // 3, radius=7, vel_x=3, vel_y=5)
        self.ball3 = Ball(WIDTH // 3, HEIGHT * 2 // 3, radius=9, vel_x=5, vel_y=3)
        self.left_paddle = Paddle(self.arena.x, self.arena.height // 2 - Paddle.DEFAULT_HEIGHT // 2, self.arena)
        self.right_paddle = Paddle(self.arena.width + self.arena.x - Paddle.DEFAULT_WIDTH, self.arena.height // 2 - Paddle.DEFAULT_HEIGHT // 2, self.arena)
        self.scorer = Scorer()
        self.components = [self.arena, self.ball1, self.ball2, self.ball3, self.left_paddle, self.right_paddle, self.scorer]

        #Create Game Graphics
        self.graphic = Animation(HEIGHT, WIDTH)

        #Create Game States
        self.menu = Menu()
        self.game = Game(self.graphic, self.components)
        self.state_manager = StateManager(game=self.game, menu=self.menu)
        self.clock = pygame.time.Clock()
        self.is_running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.VIDEORESIZE:
                pass
                # self.resize(event.w, event.h)
                # self.graphic.width = event.w
                # self.graphic.height = event.h
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.state = self.menu()
                elif event.key == pygame.K_RETURN:
                    if self.menu.selected_item == 0:  # One Player
                        self.state = self.game()
        


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

    def draw_menu(self):
        self.menu.draw()


    def run(self):

        while self.is_running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                self.state_manager.on_event(event)
            
            self.state_manager.update()
            self.state_manager.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = App()
    app.run()