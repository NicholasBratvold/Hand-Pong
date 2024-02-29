import pygame
from Pong.components import Ball, Arena, Paddle, Scorer
import math
import time
import cv2
import random
import os

# All state inherit. Treat it like a interface.
class State:
    # Only draw
    def draw(self, surface): pass
    # Process event
    def on_event(self, event): pass
    # Logic
    def on_update(self, delta, ticks): pass
    # Resize window
    def on_resize(self): pass


class Menu(State):
 
    def __init__(self, animation, mixer):
        self.menu_items = ["One Player","Two Player", "Quit"]
        self.selected_item = 0
        self.animation = animation
        self.w, self.h = self.animation.width, self.animation.height
        #20 balls
        self.balls = self.random_balls(100)
        self.animation = animation
        self.mixer = mixer


    def random_balls(self, number):
        return [Ball(random.randint(0, self.w), random.randint(0, self.h), radius=random.randint(1, 10), vel_x=random.randint(-5, 5), vel_y=random.randint(-5, 5)) for _ in range(number)]

    def draw(self):
        self.animation.draw(self.balls)
        self.animation.draw_menu(self.menu_items, self.selected_item)
        self.animation.render()
 
    def on_event(self, event):
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
        
        for ball in self.balls:
            ball.update(dt)
        self.check_collisions()
   
    def check_collisions(self):
        offset = 1

        # Check collision with top and bottom boundaries
        for i in range(len(self.balls)):
            ball1 = self.balls[i]
            #collision with boundaries
            if ball1.y - ball1.radius <= 0:
                ball1.vel_y *= -1
                ball1.y += offset 
                # self.mixer.play_sound("wall")
            
            elif ball1.y + ball1.radius >= self.h:
                ball1.vel_y *= -1
                ball1.y -= offset
                # self.mixer.play_sound("wall")

            if ball1.x - ball1.radius <= 0:
                ball1.vel_x *= -1
                ball1.x += offset
                # self.mixer.play_sound("wall")
            
            elif ball1.x + ball1.radius >= self.w:
                ball1.vel_x *= -1
                ball1.x -= offset
                # self.mixer.play_sound("wall")

            for j in range(i+1, len(self.balls)):
                ball2 = self.balls[j]
                dx = ball1.x - ball2.x
                dy = ball1.y - ball2.y
                distance = (dx**2 + dy**2)**0.5
                if distance == 0:
                    break
                if distance < ball1.radius + ball2.radius:
                    # Collision occurred
                    v1 = pygame.Vector2(ball1.vel_x, ball1.vel_y)
                    v2 = pygame.Vector2(ball2.vel_x, ball2.vel_y)
                    nv = v2-v1
                    if nv[0] <= 0.01 and nv[1] <= 0.01:
                        nv = pygame.Vector2(1, 1) 
                    new_v1 = pygame.math.Vector2(v1).reflect(nv)
                    new_v2 = pygame.math.Vector2(v2).reflect(nv)
                    ball1.vel_x = new_v1.x
                    ball1.vel_y = new_v1.y
                    ball2.vel_x = new_v2.x
                    ball2.vel_y = new_v2.y

                    # Move the balls apart
                    overlap = ball1.radius + ball2.radius - distance + offset
                    dx /= distance
                    dy /= distance
                    ball1.x += overlap / 2 * dx
                    ball1.y += overlap / 2 * dy
                    ball2.x -= overlap / 2 * dx
                    ball2.y -= overlap / 2 * dy

                    ball1.hit = True
                    ball2.hit = True
                    # self.mixer.play_sound("ball")
                    print("Collision")

    def on_resize(self, w, h):
        self.w = w
        self.h = h

class Game(State):

    def __init__(self, graphic, components, mixer, hand_tracker, face_tracker, cap, one_player=False):
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

        
        if self.one_player:
            for paddle in self.paddles:
                if paddle.x > self.arena.width // 2 + self.arena.x:
                    self.components.remove(paddle)
                    self.paddles.pop()
                    break
                

    def draw(self):

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
        
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to grab frame")
            return
        # flip the frame so it's not a mirror view
        frame = cv2.flip(frame, 1)

        # Find hands in the frame
        self.hand_tracker.find_hands(frame, draw=False)
        self.hand_landmarks = self.hand_tracker.get_landmarks()
        # Find faces in the frame
        self.face_tracker.find_faces(frame, draw=False)
        self.face_landmarks = self.face_tracker.get_landmarks()

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
        if event.type == pygame.KEYDOWN:
            for paddle in self.paddles:

                if event.key == pygame.K_UP and paddle.y - paddle.vel > self.arena.y:
                    paddle.vel = -paddle.speed
                if event.key == pygame.K_DOWN and paddle.y + paddle.vel < self.arena.y + self.arena.height - paddle.height:
                    paddle.vel = paddle.speed
        # Handle keyup events
        if event.type == pygame.KEYUP:
            for paddle in self.paddles:
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    paddle.vel = 0
        return None

    def on_resize(self, w , h):
        self.graphic.resize(w, h, self.components)
        self.graphic.width = w
        self.graphic.height = h

    def adjust_difficulty(self): 
        vel_array = [-7, -6, -5, -4, -3, 3, 4, 5, 6, 7]
        max_balls = 10
        add_ball = False
        if self.scorer.score_left > 2 * len(self.balls) and self.scorer.score_left > 0 and len(self.balls) <= max_balls:
            add_ball = True

        if add_ball:
            ball = Ball(self.arena.x + self.arena.width // 2, self.arena.y + self.arena.height // 3, radius=random.randint(5,15), vel_x=random.choice(vel_array), vel_y=random.choice(vel_array))
            self.balls.append(ball)
            self.components.append(ball)
            add_ball = False

    def update_background(self): 
        for ball in self.balls:
            # Calculate the grid indices
            col = int((ball.x - self.arena.x) // self.arena.cell_size[0])
            row = int((ball.y - self.arena.y) // self.arena.cell_size[1])
            if col < self.arena.cols and row < self.arena.rows:
                if not self.arena.grid[row][col]:
                    # Update the grid
                    self.arena.grid[row][col] = 1
                    # Add the cell to the dirty cells list
                    self.arena.dirty_cells.append((row, col))

    def check_goal(self, ball):
        offset = 1
         # Check if the ball passes the left boundary
        if ball.x - ball.radius <= self.arena.x:
            # Increment the score for the right player
            self.scorer.score_right += 1
            if self.one_player:
                self.mixer.play_sound("lose")
            else:
                self.mixer.play_sound("score")
            # Reset the ball's position
            self.reset_ball(ball)

        # Check if the ball passes the right boundary
        if self.one_player:
            if ball.x + ball.radius >= self.arena.x + self.arena.width:
                # Increment the score for the left player
                self.scorer.score_left += 1
                self.mixer.play_sound("score")
                # Reset the ball's position
                ball.vel_x *= -1
                ball.x -= offset

        elif ball.x + ball.radius >= self.arena.x + self.arena.width:
            # Increment the score for the left player
            self.scorer.score_left += 1
            self.mixer.play_sound("score")
            # Reset the ball's position
            self.reset_ball(ball)

    def reset_ball(self, ball):
        ball.x = self.arena.x + self.arena.width // 2
        ball.y = self.arena.y + self.arena.height // 2
        # Reset the ball's velocity
        ball.vel_x *= -1
        ball.vel_y *= -1

    def check_collisions(self):
        offset = 1
         # Check collision with top and bottom boundaries
        for i in range(len(self.balls)):
            ball1 = self.balls[i]
            #collision with top and bottom boundaries
            if ball1.y - ball1.radius <= self.arena.y:
                ball1.vel_y *= -1
                ball1.y += offset
                self.mixer.play_sound("wall")
            elif ball1.y + ball1.radius >= self.arena.y + self.arena.height:
                ball1.vel_y *= -1
                ball1.y -= offset
                self.mixer.play_sound("wall")

            #collisions with side boundaries
            self.check_goal(ball1)

            for paddle in self.paddles:
                # Check collision with left paddle
                if (paddle.x < self.arena.width // 2 + self.arena.x):
                    if (paddle.x + paddle.width + ball1.radius > ball1.x > paddle.x and paddle.y < ball1.y < paddle.y + paddle.height):
                        ball1.vel_x *= -1
                        ball1.x += offset
                        self.mixer.play_sound("paddle")

                # Check collision with right paddle
                if (paddle.x > self.arena.width // 2 + self.arena.x):
                    if (paddle.x - ball1.radius < ball1.x < paddle.x + paddle.width and paddle.y < ball1.y < paddle.y + paddle.height):
                        ball1.vel_x *= -1
                        ball1.x -= offset
                        self.mixer.play_sound("paddle")

                # Check if the paddle is out of bounds 
                if paddle.y < self.arena.y:
                    paddle.y = self.arena.y
                elif paddle.y + paddle.height > self.arena.y + self.arena.height:
                    paddle.y = self.arena.y + self.arena.height - paddle.height

            for j in range(i+1, len(self.balls)):
                ball2 = self.balls[j]
                dx = ball1.x - ball2.x
                dy = ball1.y - ball2.y
                distance = (dx**2 + dy**2)**0.5
                if distance == 0:
                    break
                if distance < ball1.radius + ball2.radius:
                    # Collision occurred
                    v1 = pygame.Vector2(ball1.vel_x, ball1.vel_y)
                    v2 = pygame.Vector2(ball2.vel_x, ball2.vel_y)
                    nv = v2-v1
                    if nv[0] <= 0.01 and nv[1] <= 0.01:
                        nv = pygame.Vector2(1, 1)
                    
                    new_v1 = pygame.math.Vector2(v1).reflect(nv)
                    new_v2 = pygame.math.Vector2(v2).reflect(nv)
                    ball1.vel_x = new_v1.x
                    ball1.vel_y = new_v1.y
                    ball2.vel_x = new_v2.x
                    ball2.vel_y = new_v2.y

                    # move the balls apart
                    overlap = ball1.radius + ball2.radius - distance + offset
                    dx /= distance
                    dy /= distance
                    ball1.x += overlap / 2 * dx
                    ball1.y += overlap / 2 * dy
                    ball2.x -= overlap / 2 * dx
                    ball2.y -= overlap / 2 * dy

                    ball1.hit = True
                    ball2.hit = True
                    self.mixer.play_sound("ball")
                    print("Collision")

class StateManager(State):

    def __init__(self, one_player, two_player, menu):
        self.one_player = one_player
        self.two_player = two_player
        self.menu = menu
        self.state = self.menu
        self.last_update = pygame.time.get_ticks()

    def draw(self):
        self.state.draw()

    def on_event(self, event):
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
        now = pygame.time.get_ticks()
        dt = now - self.last_update
        self.last_update = now
        print(dt)
        self.state.update(dt / 30)

    def on_resize(self, w, h):
        self.state.on_resize(w, h)


class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = {"ball": "ball.wav", "score": "score.wav", "wall": "wall_2.mp3", "paddle": "paddle.wav", "lose": "lose.wav"}
        self.load_sounds()
        # self.mixer.music.load("background.mp3")

    def load_sounds(self):

        # Get the directory of the current script
        script_dir = os.path.dirname(os.path.realpath(__file__))

        for sound in self.sounds:
        # Build the path to the sound file
            sound_file = os.path.join(script_dir, '../../sounds', self.sounds[sound])
            self.sounds[sound] = pygame.mixer.Sound(sound_file)
        
    def play_sound(self, sound):
        self.sounds[sound].play()
    
    # def play_background(self):
    #     self.mixer.music.play(-1)