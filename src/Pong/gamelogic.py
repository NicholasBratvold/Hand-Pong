import pygame
from Pong.components import Ball, Arena, Paddle, Scorer
import math

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
 
    def __init__(self):
        self.menu_items = ["One Player", "Settings", "Quit"]
        self.selected_item = 0
        self.screen = pygame.display.get_surface()
        self.w, self.h = self.screen.get_size()

    def draw(self):
        font = pygame.font.Font(None, 36)
        for index, item in enumerate(self.menu_items):
            if index == self.selected_item:
                text = font.render("-> " + item, True, (255, 255, 255))
            else:
                text = font.render(item, True, (255, 255, 255))
            self.screen.blit(text, (self.w // 2 - text.get_width() // 2, 200 + index * 50))

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected_item = (self.selected_item + 1) % len(self.menu_items)
            elif event.key == pygame.K_UP:
                self.selected_item = (self.selected_item - 1) % len(self.menu_items)
            elif event.key == pygame.K_RETURN:
                return self.selected_item
        return None

    def update(self): pass

class Game(State):

    def __init__(self, graphic, components):
        self.graphic = graphic
        self.components = components
        self.arena = None
        self.scorer = None
        self.paddles = []
        self.balls = []
        self.others = []

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
        self.graphic.draw(self.components)
    
    def update(self):
        
        for component in self.components:
            component.update()
        self.check_collisions()
        self.adjust_difficulty()
        self.update_background()
        

    def on_event(self, event):
        if event.type == pygame.VIDEORESIZE:
                pass
                # self.on_resize(event.w, event.h)
                # self.graphic.width = event.w
                # self.graphic.height = event.h
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                    self.state = self.menu() if self.state() is not self.menu() else self.game()
            elif event.key == pygame.K_RETURN:
                if self.menu.selected_item == 0:
                    self.state = self.game()
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

    def on_resize(self, w , h):
        self.graphic.resize(w, h, self.components)
        self.graphic.width = w
        self.graphic.height = h

    def adjust_difficulty(self): pass

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
        self.state = self.game

    def draw(self):
        self.state.draw()

    def on_event(self, event):
        if event.type == pygame.VIDEORESIZE:
                self.on_resize(event.w, event.h)
        elif event.type == pygame.KEYDOWN:
            if event.key == (pygame.K_ESCAPE or pygame.K_p):
                    self.state = self.menu() if self.state() is not self.menu() else self.game()

        self.state.on_event(event)    

    def update(self):
        self.state.update()

    def on_resize(self, w, h):
        self.state.on_resize(w, h)

