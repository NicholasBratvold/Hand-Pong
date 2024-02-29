import pygame
from Pong.components import Ball, Arena, Paddle, Scorer
import math
import time
import cv2
import random
import os


class State:
    """
    Base class for game states.

    Methods:
        draw(self, surface):
            Draw the state on the given surface.
        on_event(self, event):
            Process the given event.
        on_update(self, dt):
            Update the state based on the time elapsed since the last update.
        on_resize(self):
            Resize the window.
    """

    def draw(self, surface):
        """
        Draw the state on the given surface.

        Args:
            surface (pygame.Surface): The surface to draw on.
        """
        pass

    def on_event(self, event):
        """
        Process the given event.

        Args:
            event (pygame.event.Event): The event to process.
        """
        pass

    def on_update(self, dt):
        """
        Update the state based on the time elapsed since the last update.

        Args:
            dt (float): The time elapsed since the last update.
        """
        pass

    def on_resize(self):
        """
        Resize the window.
        """
        pass


class Menu(State):
    """
    Represents the menu state of the game.

    Attributes:
        menu_items (list): A list of menu items.
        selected_item (int): The index of the selected menu item.
        animation (Animation): The animation object.
        balls (list): A list of random balls.
        mixer (Mixer): The sound mixer object.

    Methods:
        __init__(self, animation, mixer):
            Initialize the Menu state.
        draw(self):
            Draw the menu state using the Animation object.
        on_event(self, event):
            Move the menu selection based on keyboard input. Press return to select an item.
        update(self, dt):
            Update the balls in the menu window according to the time elapsed since the last update.
        check_collisions(self):
            Check for collisions between balls and boundaries or other balls.
        on_resize(self, w, h):
            Resize the window.
    """

    def __init__(self, animation, mixer):
        """
        Initialize the Menu state.

        Args:
            animation (Animation): The animation object.
            mixer (Mixer): The mixer object.
        """
        self.menu_items = ["One Player", "Two Player", "Quit"]
        self.selected_item = 0
        self.animation = animation
        self.w, self.h = self.animation.width, self.animation.height
        self.balls = self.random_balls(100)
        self.animation = animation
        self.mixer = mixer

    def random_balls(self, number):
        """
        Generate a list of random balls.

        Args:
            number (int): The number of balls to generate.

        Returns:
            list: A list of Ball objects.
        """
        return [
            Ball(
                random.randint(0, self.w),
                random.randint(0, self.h),
                radius=random.randint(4, 15),
                vel_x=random.randint(-5, 5),
                vel_y=random.randint(-5, 5),
            )
            for _ in range(number)
        ]

    def draw(self):
        """
        Draw the menu state using the Animation object.
        """
        self.animation.draw(self.balls)
        self.animation.draw_menu(self.menu_items, self.selected_item)
        self.animation.render()

    def on_event(self, event):
        """
        Move the menu selection based on keyboard input. Press return to select an item.
        If the selected item is "Quit", the game will exit.

        Args:
            event (pygame.event.Event): The event to process.

        Returns:
            str: The selected menu item.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN:
                if self.selected_item == 2:
                    pygame.quit()
                    quit()
                if self.selected_item == 0:
                    return "One Player"
                if self.selected_item == 1:
                    return "Two Player"
                else:
                    pass

    def update(self, dt):
        """
        Update the balls in the menu window according to the time elapsed since the last update.

        Args:
            dt (float): The time elapsed since the last update.
        """
        for ball in self.balls:
            ball.update(dt)
        self.check_collisions()

    def check_collisions(self):
        """
        Check for collisions between balls and boundaries or other balls.

        Ball to ball collisions are perfectly elastic and their mass is proportional to their area.
        """

        # offset to prevent balls from getting stuck in the boundaries
        offset = 1

        for i in range(len(self.balls)):
            ball1 = self.balls[i]
            # collision with walls
            if ball1.y - ball1.radius <= 0 and ball1.vel_y < 0:
                ball1.vel_y *= -1
                ball1.y += offset

            elif ball1.y + ball1.radius >= self.h and ball1.vel_y > 0:
                ball1.vel_y *= -1
                ball1.y -= offset

            if ball1.x - ball1.radius <= 0 and ball1.vel_x < 0:
                ball1.vel_x *= -1
                ball1.x += offset

            elif ball1.x + ball1.radius >= self.w and ball1.vel_x > 0:
                ball1.vel_x *= -1
                ball1.x -= offset

            # collision with other balls
            for j in range(i + 1, len(self.balls)):
                ball2 = self.balls[j]

                # skip if both balls have recently been hit
                if ball1.hit and ball2.hit:
                    continue

                dx = ball1.x - ball2.x
                dy = ball1.y - ball2.y
                distance = (dx**2 + dy**2) ** 0.5

                if distance < ball1.radius + ball2.radius:
                    v1 = pygame.Vector2(ball1.vel_x, ball1.vel_y)
                    v2 = pygame.Vector2(ball2.vel_x, ball2.vel_y)

                    m1 = ball1.radius**2
                    m2 = ball2.radius**2

                    # Elastic Collision
                    v1f = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
                    v2f = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)

                    ball1.vel_x = v1f.x
                    ball1.vel_y = v1f.y
                    ball2.vel_x = v2f.x
                    ball2.vel_y = v2f.y

                    ball1.hit = True
                    ball2.hit = True

    def on_resize(self, w, h):
        """
        Resize the window.

        Args:
            w (int): The new width of the window.
            h (int): The new height of the window.
        """
        self.w = w
        self.h = h
        self.animation.resize(w, h, self.balls)


class Game(State):
    """
    Represents the game state of the game.

    Attributes:
        graphic (Animation): The animation object.
        components (list): A list of game components.
        mixer (Mixer): The sound mixer object.
        hand_tracker (HandTracker): The hand tracker object.
        face_tracker (FaceTracker): The face tracker object.
        cap (cv2.VideoCapture): The video capture object.
        one_player (bool, optional): Whether the game is in one player mode. Defaults to False.
        arena (Arena): The arena object.
        scorer (Scorer): The scorer object.
        paddles (list): A list of paddle objects.
        balls (list): A list of ball objects.
        others (list): A list of other game components.
        frame_start_time (float): The start time of the current frame.
        fps (float): The frames per second of the game.

    Methods:
        __init__(self, graphic, components, mixer, hand_tracker, face_tracker, cap, one_player=False):
            Initialize the Game state.
        draw(self):
            Draw the game state.
        update(self, dt):
            Update the game state.
        on_event(self, event):
            Handles keyboard arrow inputs to move the paddles.
        on_resize(self, w, h):
            Resize the window.
        adjust_difficulty(self):
            Adjust the game difficulty based on the score.
        update_background(self):
            Update the background of the game.
        check_goal(self, ball):
            Check if the ball passes the boundaries and update the score.
        reset_ball(self, ball):
            Reset the ball's position and velocity.
        check_collisions(self):
            Check for collisions between the balls, paddles, and boundaries.
    """

    def __init__(
        self,
        graphic,
        components,
        mixer,
        hand_tracker,
        face_tracker,
        cap,
        one_player=False,
    ):
        """
        Initialize the Game state.

        Args:
            graphic (Animation): The animation object.
            components (list): A list of game components.
            mixer (Mixer): The sound mixer object.
            hand_tracker (HandTracker): The hand tracker object.
            face_tracker (FaceTracker): The face tracker object.
            cap (cv2.VideoCapture): The video capture object.
            one_player (bool, optional): Whether the game is in one player mode. Defaults to False.
        """
        self.graphic = graphic
        self.components = [c.copy() for c in components]
        self.one_player = one_player
        self.arena = None
        self.scorer = None
        self.paddles = []
        self.balls = []
        self.others = []

        self.frame_start_time = None
        self.fps = 0

        self.mixer = mixer

        self.hand_tracker = hand_tracker
        self.face_tracker = face_tracker
        self.cap = cap
        self.hand_landmarks = None
        self.face_landmarks = None

        # Parse the components
        for component in self.components:
            if isinstance(component, Arena):
                self.arena = component
            elif isinstance(component, Scorer):
                self.scorer = component
            elif isinstance(component, Ball):
                self.balls.append(component)
            elif isinstance(component, Paddle):
                self.paddles.append(component)
            else:
                self.others.append(component)

        # Remove right paddle if in one player mode
        if self.one_player:
            for paddle in self.paddles:
                if paddle.x > self.arena.width // 2 + self.arena.x:
                    self.components.remove(paddle)
                    self.paddles.pop()
                    break

    def draw(self):
        """
        Draw the game state.
        """

        # compute FPS
        if self.frame_start_time is not None:
            time_diff = time.time() - self.frame_start_time
            self.fps = 1 / time_diff if time_diff > 0 else 0
        self.frame_start_time = time.time()

        self.graphic.draw(self.components)
        self.graphic.draw_hand_landmarks(self.hand_landmarks, self.arena)
        self.graphic.draw_face_landmarks(self.face_landmarks, self.arena)
        self.graphic.draw_fps(self.fps)
        self.graphic.render()

    def update(self, dt):
        """
        Update the game state.

        Args:
            dt (float): The time elapsed since the last update.
        """

        # Read frame from camera
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to grab frame")
            return
        frame = cv2.flip(frame, 1)

        self.hand_tracker.find_hands(frame, draw=False)
        self.hand_landmarks = self.hand_tracker.get_landmarks()
        self.face_tracker.find_faces(frame, draw=False)
        self.face_landmarks = self.face_tracker.get_landmarks()

        # Update the paddles based on detected hand landmarks
        for paddle in self.paddles:
            if paddle.x < self.arena.width // 2 + self.arena.x:
                left = True
            else:
                left = False
            if self.hand_landmarks:
                for hand_landmark in self.hand_landmarks:
                    hand_x = hand_landmark.landmark[0].x * self.arena.width
                    hand_y = hand_landmark.landmark[0].y * self.arena.height
                    if hand_x < self.arena.width // 2 and left:
                        paddle.vel = (hand_y - paddle.y) / dt
                        break
                    elif hand_x > self.arena.width // 2 and not left:
                        paddle.vel = (hand_y - paddle.y) / dt
                        break

        self.update_background()
        for component in self.components:
            component.update(dt)
        self.check_collisions()
        self.adjust_difficulty()

    def on_event(self, event):
        """
        Handles keyboard arrow inputs to move the paddles.

        Args:
            event (pygame.event.Event): The event to process.

        Returns:
            None
        """
        if event.type == pygame.KEYDOWN:
            for paddle in self.paddles:
                if event.key == pygame.K_UP and paddle.y - paddle.vel > self.arena.y:
                    paddle.vel = -paddle.speed
                if (
                    event.key == pygame.K_DOWN
                    and paddle.y + paddle.vel
                    < self.arena.y + self.arena.height - paddle.height
                ):
                    paddle.vel = paddle.speed
        if event.type == pygame.KEYUP:
            for paddle in self.paddles:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    paddle.vel = 0
        return None

    def on_resize(self, w, h):
        """
        Resize the window.

        Args:
            w (int): The new width of the window.
            h (int): The new height of the window.
        """
        self.graphic.resize(w, h, self.components)
        self.graphic.width = w
        self.graphic.height = h

    def adjust_difficulty(self):
        """
        Adjust the game difficulty based on the score.

        New balls are added to the game when the left player's score is greater than the number of balls squared.

        The new ball has randomly generated velocities and sizes from predefined lists.

        Max number of balls is 10.
        """
        vel_array = [-7, -6, -5, -4, -3, 3, 4, 5, 6, 7]
        max_balls = 10
        add_ball = False
        if (
            self.scorer.score_left > len(self.balls) ** 2 + 1
            and self.scorer.score_left > 0
            and len(self.balls) <= max_balls
        ):
            add_ball = True

        if add_ball:
            ball = Ball(
                self.arena.x + self.arena.width // 2,
                self.arena.y + self.arena.height // 3,
                radius=random.randint(5, 15),
                vel_x=random.choice(vel_array),
                vel_y=random.choice(vel_array),
            )
            self.balls.append(ball)
            self.components.append(ball)
            add_ball = False

    def update_background(self):
        """
        Update the background of the game.

        The balls position adds an alive cell to the background grid. The alive cells are used in Conway's Game of Life to create a dynamic background.
        """
        for ball in self.balls:
            col = int((ball.x - self.arena.x) // self.arena.cell_size[0])
            row = int((ball.y - self.arena.y) // self.arena.cell_size[1])
            if col < self.arena.cols and row < self.arena.rows:
                if not self.arena.grid[row][col]:
                    self.arena.grid[row][col] = 1
                    self.arena.dirty_cells.append(
                        (row, col)
                    )  # mark cell as dirty for drawing

    def check_goal(self, ball):
        """
        Check if the ball passes the boundaries and update the score.

        Args:
            ball (Ball): The ball object.
        """

        # offset to prevent balls from getting stuck in the boundaries
        offset = 1

        if ball.x - ball.radius <= self.arena.x:
            self.scorer.score_right += 1
            sound = "lose" if self.one_player else "score"
            self.mixer.play_sound(sound)
            self.reset_ball(ball)

        if ball.x + ball.radius >= self.arena.x + self.arena.width:
            self.scorer.score_left += 1
            if self.one_player:
                ball.vel_x *= -1
                ball.x -= offset
            self.mixer.play_sound("score")
            if not self.one_player:
                self.reset_ball(ball)

    def reset_ball(self, ball):
        """
        Reset the ball's position and velocity.

        Args:
            ball (Ball): The ball object.
        """
        ball.x = self.arena.x + self.arena.width // 2
        ball.y = self.arena.y + self.arena.height // 2
        ball.vel_x *= -1
        ball.vel_y *= -1

    def check_collisions(self):
        """
        Check for collisions between balls and boundaries or other balls.

        Ball to ball collisions are perfectly elastic and their mass is proportional to their area.
        """
        # offset to prevent balls from getting stuck in the boundaries
        offset = 1

        for i in range(len(self.balls)):
            ball1 = self.balls[i]

            # collisions with walls and goals
            if ball1.y - ball1.radius <= self.arena.y and ball1.vel_y < 0:
                ball1.vel_y *= -1
                ball1.y += offset
                self.mixer.play_sound("wall")
            elif (
                ball1.y + ball1.radius >= self.arena.y + self.arena.height
                and ball1.vel_y > 0
            ):
                ball1.vel_y *= -1
                ball1.y -= offset
                self.mixer.play_sound("wall")
            self.check_goal(ball1)

            for paddle in self.paddles:
                # Check collision with left paddle
                if paddle.x < self.arena.width // 2 + self.arena.x:
                    if (
                        paddle.x + paddle.width + ball1.radius > ball1.x > paddle.x
                        and paddle.y < ball1.y < paddle.y + paddle.height
                        and ball1.vel_x < 0
                    ):
                        ball1.vel_x *= -1
                        ball1.x += offset
                        self.mixer.play_sound("paddle")
                        paddle.hit = True

                # Check collision with right paddle
                if paddle.x > self.arena.width // 2 + self.arena.x:
                    if (
                        paddle.x - ball1.radius < ball1.x < paddle.x + paddle.width
                        and paddle.y < ball1.y < paddle.y + paddle.height
                        and ball1.vel_x > 0
                    ):
                        ball1.vel_x *= -1
                        ball1.x -= offset
                        self.mixer.play_sound("paddle")
                        paddle.hit = True

                # Check if the paddle is out of bounds
                if paddle.y < self.arena.y:
                    paddle.y = self.arena.y
                elif paddle.y + paddle.height > self.arena.y + self.arena.height:
                    paddle.y = self.arena.y + self.arena.height - paddle.height

            # collision with other balls
            for j in range(i + 1, len(self.balls)):

                ball2 = self.balls[j]
                # skip if both balls have recently been hit
                if ball1.hit and ball2.hit:
                    continue
                dx = ball1.x - ball2.x
                dy = ball1.y - ball2.y
                distance = (dx**2 + dy**2) ** 0.5
                if distance < ball1.radius + ball2.radius:
                    # Collision occurred
                    v1 = pygame.Vector2(ball1.vel_x, ball1.vel_y)
                    v2 = pygame.Vector2(ball2.vel_x, ball2.vel_y)

                    m1 = ball1.radius**2
                    m2 = ball2.radius**2

                    # Elastic Collision
                    v1f = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
                    v2f = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)

                    ball1.vel_x = v1f.x
                    ball1.vel_y = v1f.y
                    ball2.vel_x = v2f.x
                    ball2.vel_y = v2f.y

                    ball1.hit = True
                    ball2.hit = True
                    self.mixer.play_sound("ball")
                    # print("Collision")


class StateManager(State):
    """
    Manages the game states.

    Attributes:
        one_player (State): The one player game state.
        two_player (State): The two player game state.
        menu (State): The menu state.
        state (State): The current state.
        last_update (int): The time of the last update.

    Methods:
        __init__(self, one_player, two_player, menu):
            Initialize the StateManager.
        draw(self):
            Draw the current state.
        on_event(self, event):
            Process the given event.
        update(self):
            Update the current state.
        on_resize(self, w, h):
            Resize the window.
    """

    def __init__(self, one_player, two_player, menu):
        """
        Initialize the StateManager.

        Args:
            one_player (State): The one player game state.
            two_player (State): The two player game state.
            menu (State): The menu state.
        """
        self.one_player = one_player
        self.two_player = two_player
        self.menu = menu
        self.state = self.menu
        self.last_update = pygame.time.get_ticks()

    def draw(self):
        """
        Draw the current state.
        """
        self.state.draw()

    def on_event(self, event):
        """
        Process the given event.

        Resizes window and changes the state based on the menu selection.

        Args:
            event (pygame.event.Event): The event to process.
        """

        if event.type == pygame.VIDEORESIZE:
            self.on_resize(event.w, event.h)
        elif event.type == pygame.KEYDOWN:
            if event.key == (pygame.K_ESCAPE or pygame.K_p):
                self.state = self.menu if self.state is not self.menu else self.state

        state_code = self.state.on_event(event)

        if state_code == "One Player":
            self.state = self.one_player
        if state_code == "Two Player":
            self.state = self.two_player

    def update(self):
        """
        Update the current state according to the time elapsed since the last update.
        """
        now = pygame.time.get_ticks()
        dt = now - self.last_update
        self.last_update = now
        # print(dt)
        self.state.update(dt / 30)

    def on_resize(self, w, h):
        """
        Resize the window for every state.

        Args:
            w (int): The new width of the window.
            h (int): The new height of the window.
        """
        self.one_player.on_resize(w, h)
        self.two_player.on_resize(w, h)
        self.menu.on_resize(w, h)


class SoundManager:
    """
    Manages the game sounds.

    Attributes:
        sounds (dict): A dictionary of sound file names.
        mixer (pygame.mixer): The mixer object.

    Methods:
        __init__(self):
            Initialize the SoundManager.
        load_sounds(self):
            Load the sound files.
        play_sound(self, sound):
            Play the given sound.
    """

    def __init__(self):
        """
        Initialize the SoundManager.
        """
        pygame.mixer.init()
        self.sounds = {
            "ball": "ball.wav",
            "score": "score.wav",
            "wall": "wall_2.mp3",
            "paddle": "paddle.wav",
            "lose": "lose.wav",
        }
        self.load_sounds()
        # self.mixer.music.load("background.mp3")

    def load_sounds(self):
        """
        Load the sound files.
        """
        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.realpath(__file__))

        for sound in self.sounds:
            # Build the path to the sound file
            sound_file = os.path.join(script_dir, "../../sounds", self.sounds[sound])
            self.sounds[sound] = pygame.mixer.Sound(sound_file)

    def play_sound(self, sound):
        """
        Play the given sound.

        Args:
            sound (str): The name of the sound file to play
        """
        self.sounds[sound].play()

    def play_background(self):
        """
        Play the background music on loop.
        """
        self.mixer.music.play(-1)
