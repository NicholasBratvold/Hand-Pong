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
FPS = 60


class App:
    """
    Represents the main application for the Hand Pong game.

    Attributes:
    - arena (Arena): The game arena.
    - ball1 (Ball): The first ball in the game.
    - left_paddle (Paddle): The left paddle in the game.
    - right_paddle (Paddle): The right paddle in the game.
    - scorer (Scorer): The scorer for the game.
    - components (list): A list of game components.
    - cap (cv2.VideoCapture): The camera capture object.
    - graphic_one (Animation): The one player game graphic.
    - graphic_two (Animation): The two player game graphic.
    - menu_animation (Animation): The menu animation graphic.
    - sound_manager (SoundManager): The sound manager for the game.
    - hand_tracker (HandTracker): The hand tracker object.
    - face_tracker (FaceTracker): The face tracker object.
    - menu (Menu): The game menu state.
    - one_player (Game): The one-player game state.
    - two_player (Game): The two-player game state.
    - state_manager (StateManager): The state manager for the game.
    - clock (pygame.time.Clock): The game clock.
    - is_running (bool): Flag indicating if the game is running.
    - profile (bool): Flag indicating if profiling is enabled.
    - profiler (cProfile.Profile): The profiler object.
    """

    def __init__(self, profile=False):
        """
        Initializes the App object.

        Parameters:
        - profile (bool): Flag indicating if profiling is enabled.
        """
        # start pygame
        pygame.init()

        # Create Game Components
        self.arena = Arena(WIDTH, HEIGHT)
        self.ball1 = Ball(WIDTH // 2, HEIGHT // 2, radius=12)
        self.left_paddle = Paddle(
            self.arena.x,
            self.arena.height // 2 - Paddle.DEFAULT_HEIGHT // 2,
            self.arena,
        )
        self.right_paddle = Paddle(
            self.arena.width + self.arena.x - Paddle.DEFAULT_WIDTH,
            self.arena.height // 2 - Paddle.DEFAULT_HEIGHT // 2,
            self.arena,
        )
        self.scorer = Scorer()
        self.components = [
            self.ball1,
            self.left_paddle,
            self.right_paddle,
            self.scorer,
            self.arena,
        ]

        # Initialize Camera
        self.cap = cv2.VideoCapture(0)

        # Create Game Graphics
        self.graphic_one = Animation(HEIGHT, WIDTH)
        self.graphic_two = Animation(HEIGHT, WIDTH)
        self.menu_animation = Animation(HEIGHT, WIDTH)

        # Load sounds
        self.sound_manager = SoundManager()

        # Create Hand and Face Trackers
        self.hand_tracker = HandTracker()
        self.face_tracker = FaceTracker()

        # Create Game States
        self.menu = Menu(self.menu_animation, self.sound_manager)
        self.one_player = Game(
            self.graphic_one,
            self.components,
            self.sound_manager,
            self.hand_tracker,
            self.face_tracker,
            self.cap,
            one_player=True,
        )
        self.two_player = Game(
            self.graphic_two,
            self.components,
            self.sound_manager,
            self.hand_tracker,
            self.face_tracker,
            self.cap,
        )
        self.state_manager = StateManager(
            self.one_player, self.two_player, menu=self.menu
        )
        self.clock = pygame.time.Clock()
        self.is_running = True

        # Profiler
        self.profile = profile
        if self.profile == True:
            self.profiler = cProfile.Profile()

    def exit_game(self):
        """
        Exits the game by quitting pygame, releasing the camera capture, closing the hand and face trackers, closing the sound manager,
        and exiting the program.
        """
        pygame.quit()
        self.cap.release()
        cv2.destroyAllWindows()
        self.hand_tracker.close()
        self.face_tracker.close()
        sys.exit()

    def run(self):
        """
        Runs the game loop until the game is exited.
        """
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
    app = App(profile=False)
    app.run()
