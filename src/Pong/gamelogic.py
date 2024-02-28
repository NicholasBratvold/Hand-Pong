import pygame
from Pong.components import Ball, Arena, Paddle, Scorer
import math
import time
import cv2
import random

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
 
    def __init__(self, animation):
        self.menu_items = ["Start", "Quit"]
        self.selected_item = 0
        self.animation = animation
        self.w, self.h = self.animation.width, self.animation.height
        #20 balls
        self.balls = self.random_balls(100)
        self.animation = animation

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
                if self.selected_item == 1:
                    pygame.quit()
                    quit()
                if self.selected_item == 0:
                    return "Start"
                else:
                    pass

    def update(self):
        
        for ball in self.balls:
            ball.update()
        self.check_collisions()
   
    def check_collisions(self):
        # Check collision with top and bottom boundaries
        for i in range(len(self.balls)):
            ball1 = self.balls[i]
            #collision with boundaries
            if ball1.y - ball1.radius <= 0 or ball1.y + ball1.radius >= self.h:
                ball1.vel_y *= -1
            if ball1.x - ball1.radius <= 0 or ball1.x + ball1.radius >= self.w:
                ball1.vel_x *= -1
            
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
                    new_v1 = pygame.math.Vector2(v1).reflect(nv)
                    new_v2 = pygame.math.Vector2(v2).reflect(nv)
                    ball1.vel_x = new_v1.x
                    ball1.vel_y = new_v1.y
                    ball2.vel_x = new_v2.x
                    ball2.vel_y = new_v2.y
                    print("Collision")

    def on_resize(self, w, h):
        self.w = w
        self.h = h

class Game(State):

    def __init__(self, graphic, components, hand_tracker, face_tracker, cap):
        self.graphic = graphic
        self.components = components
        self.arena = None
        self.scorer = None
        self.paddles = []
        self.balls = []
        self.others = []

        self.frame_start_time = None
        self.fps = 0


        self.hand_tracker = hand_tracker
        self.face_tracker = face_tracker
        self.cap = cap
        self.hand_landmarks = None
        self.face_landmarks = None

        for component in components:
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
    
    def update(self):
        
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
                    if hand_landmark.landmark[0].x * self.arena.width < self.arena.width // 2 and left:
                        paddle.y = hand_landmark.landmark[0].y * self.arena.height
                        break
                    elif hand_landmark.landmark[0].x * self.arena.width > self.arena.width // 2 and not left:
                        paddle.y = hand_landmark.landmark[0].y * self.arena.height
                        break
            

        for component in self.components:
            component.update()
        
        self.check_collisions()
        self.adjust_difficulty()
        self.update_background()

        

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
    
        add_ball = False
        if self.scorer.score_left % 2 == 0 and self.scorer.score_left > len(self.balls) and self.scorer.score_left > 0:
            for ball in self.balls:
                ball.vel_x +=random.randint(-1, 1)
                ball.vel_y +=random.randint(-1, 1)
            add_ball = True

        if add_ball:
            ball = Ball(self.arena.x + self.arena.width // 2, self.arena.y + self.arena.height // 2, radius=random.randint(3,7), vel_x=5, vel_y=5)
            self.balls.append(ball)
            self.components.append(ball)
            add_ball = False

    def update_background(self): 
        for ball in self.balls:
            # Calculate the grid indices
            col = int((ball.x - self.arena.x) // self.arena.cell_size[0])
            row = int((ball.y - self.arena.y) // self.arena.cell_size[1])
            if col < self.arena.cols and row < self.arena.rows:
                # Update the grid
                self.arena.grid[row][col] = 1

    def check_goal(self, ball):
         # Check if the ball passes the left boundary
        if ball.x - ball.radius <= self.arena.x:
            # Increment the score for the right player
            self.scorer.score_right += 1
            # Reset the ball's position
            self.reset_ball(ball)

        # Check if the ball passes the right boundary
        if ball.x + ball.radius >= self.arena.x + self.arena.width:
            # Increment the score for the left player
            self.scorer.score_left += 1
            # Reset the ball's position
            self.reset_ball(ball)

    def reset_ball(self, ball):
        ball.x = self.arena.x + self.arena.width // 2
        ball.y = self.arena.y + self.arena.height // 2
        # Reset the ball's velocity
        ball.vel_x *= -1
        ball.vel_y *= -1

    def check_collisions(self):
         # Check collision with top and bottom boundaries
        for i in range(len(self.balls)):
            ball1 = self.balls[i]
            #collision with top and bottom boundaries
            if ball1.y <= self.arena.y + ball1.radius or ball1.y >= self.arena.y + self.arena.height - ball1.radius:
                ball1.vel_y *= -1

            #collisions with side boundaries
            self.check_goal(ball1)

            for paddle in self.paddles:
                # Check collision with left paddle
                if (paddle.x < self.arena.width // 2 + self.arena.x):
                    if (paddle.x + paddle.width + ball1.radius > ball1.x > paddle.x and paddle.y < ball1.y < paddle.y + paddle.height):
                        ball1.vel_x *= -1

                # Check collision with right paddle
                if (paddle.x > self.arena.width // 2 + self.arena.x):
                    if (paddle.x - ball1.radius < ball1.x < paddle.x + paddle.width and paddle.y < ball1.y < paddle.y + paddle.height):
                        ball1.vel_x *= -1

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
                    print(nv)
                    new_v1 = pygame.math.Vector2(v1).reflect(nv)
                    new_v2 = pygame.math.Vector2(v2).reflect(nv)
                    ball1.vel_x = new_v1.x
                    ball1.vel_y = new_v1.y
                    ball2.vel_x = new_v2.x
                    ball2.vel_y = new_v2.y
                    print("Collision")

class StateManager(State):

    def __init__(self, game, menu):
        self.game = game
        self.menu = menu
        self.state = self.menu

    def draw(self):
        self.state.draw()

    def on_event(self, event):
        if event.type == pygame.VIDEORESIZE:
                self.on_resize(event.w, event.h)
        elif event.type == pygame.KEYDOWN:
            if event.key == (pygame.K_ESCAPE or pygame.K_p):
                self.state = self.menu if self.state is not self.menu else self.game
        state_code = self.state.on_event(event)

        if state_code == "Start":
            self.state = self.game

    def update(self):
        self.state.update()

    def on_resize(self, w, h):
        self.state.on_resize(w, h)

