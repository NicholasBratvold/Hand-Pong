import pygame
import sys
from Pong.components import Ball, Arena, Paddle, Scorer
from Pong.gamelogic import Game, StateManager, Menu, SoundManager
from Pong.graphics import Animation
from Tracker.handtracker import HandTracker, FaceTracker
import cv2

import cProfile

WIDTH = 1600
HEIGHT = 1200
FPS = 90


class App:
    def __init__(self, profile=False):
        pygame.init()
        
        #Create Game Components
        self.arena = Arena(WIDTH, HEIGHT)
        self.ball1 = Ball(WIDTH // 2, HEIGHT // 2, radius=12)
        self.left_paddle = Paddle(self.arena.x, self.arena.height // 2 - Paddle.DEFAULT_HEIGHT // 2, self.arena)
        self.right_paddle = Paddle(self.arena.width + self.arena.x - Paddle.DEFAULT_WIDTH, self.arena.height // 2 - Paddle.DEFAULT_HEIGHT // 2, self.arena)
        self.scorer = Scorer()
        self.components = [self.ball1, self.left_paddle, self.right_paddle, self.scorer, self.arena]

        #Initialize Camera
        self.cap = cv2.VideoCapture(0)

        #Create Game Graphics
        self.graphic_one = Animation(HEIGHT, WIDTH)
        self.graphic_two = Animation(HEIGHT, WIDTH)
        self.menu_animation = Animation(HEIGHT, WIDTH)

        #Load sounds
        self.sound_manager = SoundManager()

    
        #Create Hand and Face Trackers
        self.hand_tracker = HandTracker()
        self.face_tracker = FaceTracker()

        #Create Game States
        self.menu = Menu(self.menu_animation, self.sound_manager)
        self.one_player = Game(self.graphic_one, self.components, self.sound_manager, self.hand_tracker, self.face_tracker, self.cap, one_player=True)
        self.two_player = Game(self.graphic_two, self.components, self.sound_manager, self.hand_tracker, self.face_tracker, self.cap)
        self.state_manager = StateManager(self.one_player, self.two_player, menu=self.menu)
        self.clock = pygame.time.Clock()
        self.is_running = True

        #profiler
        self.profile = profile
        if self.profile == True:
            self.profiler = cProfile.Profile()

    def exit_game(self):
        pygame.quit()
        self.cap.release()
        cv2.destroyAllWindows()
        self.hand_tracker.close()
        self.face_tracker.close()
        sys.exit()

    def run(self):

        if self.profile:
                self.profiler.enable()

        while self.is_running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                self.state_manager.on_event(event)
            
            self.state_manager.update()
            self.state_manager.draw()
            self.clock.tick(FPS)

        if self.profile:
            self.profiler.disable()
            self.profiler.print_stats()
            
        self.exit_game()

if __name__ == "__main__":
    app = App(profile=True)
    app.run()