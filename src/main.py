import pygame
import sys
from Pong.components import Ball, Arena, Paddle, Scorer
from Pong.gamelogic import Game, StateManager, Menu
from Pong.graphics import Animation
from handtracker import HandTracker, FaceTracker
import cv2


WIDTH = 1600
HEIGHT = 1200
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
        self.left_paddle = Paddle(self.arena.x, self.arena.height // 2 - Paddle.DEFAULT_HEIGHT // 2, self.arena)
        self.right_paddle = Paddle(self.arena.width + self.arena.x - Paddle.DEFAULT_WIDTH, self.arena.height // 2 - Paddle.DEFAULT_HEIGHT // 2, self.arena)
        self.scorer = Scorer()
        self.components = [self.arena, self.ball1, self.left_paddle, self.right_paddle, self.scorer]

        #Initialize Camera
        self.cap = cv2.VideoCapture(0)

        #Create Game Graphics
        self.graphic = Animation(HEIGHT, WIDTH)
        self.menu_animation = Animation(HEIGHT, WIDTH)
    
        #Create Hand and Face Trackers
        self.hand_tracker = HandTracker()
        self.face_tracker = FaceTracker()

        #Create Game States
        self.menu = Menu(self.menu_animation)
        self.game = Game(self.graphic, self.components, self.hand_tracker, self.face_tracker, self.cap)
        self.state_manager = StateManager(game=self.game, menu=self.menu)
        self.clock = pygame.time.Clock()
        self.is_running = True


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
        self.cap.release()
        cv2.destroyAllWindows()
        self.hand_tracker.close()
        self.face_tracker.close()
        sys.exit()

if __name__ == "__main__":
    app = App()
    app.run()