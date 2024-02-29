import random
import pygame
from Pong.components import Ball, Arena, Paddle, Scorer
import math

class Animation:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.arena_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)  # Surface for the arena
        self.draw_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.display.set_caption("Pong")


    def draw(self, components):
        self.draw_surf.fill((0,0,0,220))
        for component in components:
            self.draw_component(component)

    def render(self):
        self.screen.blit(self.arena_surf, (0,0))
        self.screen.blit(self.draw_surf, (0,0))
        pygame.display.flip()

    def draw_component(self, component):
        if type(component) is Ball:
            self.draw_ball(component)
        elif type(component) is Paddle:
            self.draw_paddle(component)
        elif type(component) is Arena:
            self.draw_arena(component)
        elif type(component) is Scorer:
            self.draw_scorer(component)
        else:
            print("No draw method for class: ", type(component))
    
    def draw_hand_landmarks(self, landmarks, arena):
        scale = 0.2
        if landmarks:
            for hand in landmarks:
                x_0, y_0 = hand.landmark[0].x * self.width, hand.landmark[0].y * arena.height
                for landmark in hand.landmark:
                    x, y = int(landmark.x * arena.width * scale), int(landmark.y * arena.height * scale)
                    pygame.draw.circle(self.draw_surf, (100, 0, 0), (x + x_0, y + y_0), 3)

    def draw_face_landmarks(self, landmarks, arena):
        scale = 0.2
        if landmarks:
            for detection in landmarks:
                x_0, y_0 = detection.location_data.relative_keypoints[0].x * self.width, detection.location_data.relative_keypoints[0].y * arena.height - arena.height// 2
                for index, landmark in enumerate(detection.location_data.relative_keypoints):
                    x, y = int(landmark.x * self.width * scale), int(landmark.y * self.height * scale)
                    
                    # Eyes
                    if index in [0, 1]:  # indices for left and right eye center
                        pygame.draw.circle(self.draw_surf, (0, 100, 0), (x + x_0, y + y_0), 10, 2)
                        pygame.draw.circle(self.draw_surf, (0, 255, 0), (x + x_0 + 10* math.sin(math.pi/x_0), y + y_0 + 3), 3)
                    
                    # Nose
                    elif index == 2: 
                        pygame.draw.ellipse(self.draw_surf, (0, 100, 0), (x + x_0 - 2.5, y + y_0 - 15, 5, 15))
                    
                    # Mouth
                    elif index == 3:
                        pygame.draw.arc(self.draw_surf, (0, 100, 0), (x + x_0 - 15, y + y_0, 30, 20), 0, math.pi, 2)

                    # Ears
                    else:
                        pygame.draw.ellipse(self.draw_surf, (0, 100, 0), (x + x_0 - 2.5, y + y_0 - 15, 5, 15))
                        

    def draw_fps(self, fps):

        fps_text = f"FPS: {math.floor(fps)}"
        self.font = pygame.font.SysFont(None, 24)

        text_render = self.font.render(fps_text, True, (255, 255, 255))
        text_rect = text_render.get_rect()
        text_rect.topleft = (10, 20) 
        self.draw_surf.blit(text_render, text_rect)

    def draw_menu(self, menu_items, selected_item):
        #add transparency to the menu
        self.menu_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.menu_surf.fill((0,0,0,100))

        font = pygame.font.SysFont(None, 36)
        for i, item in enumerate(menu_items):
            if i == selected_item:
                color = (255, 0, 0)
            else:
                color = (255, 255, 255)
            text = font.render(item, True, color)
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2 + i * 50))
            self.menu_surf.blit(text, text_rect)
            self.draw_surf.blit(self.menu_surf, (0,0))

    def resize(self, w, h, components):
        width_ratio = w / self.width
        height_ratio = h / self.height
        self.width = w
        self.height = h
        for component in components: 
            component.resize(width_ratio, height_ratio)
        self.arena_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.screen.fill((0,0,0))
        self.render()
        

    def draw_ball(self, ball):
         # Draw the tail circles with changing colors
        tail_length = len(ball.tail_positions)
        tail_factor = 255 // tail_length
        for i, (x, y) in enumerate(reversed(ball.tail_positions)):
            if i >= tail_length:
                break
            wiggle = 5  # Adjust this value to change the amount of wiggle
            x += math.cos(x * 0.1) * wiggle
            y += math.sin(y * 0.1) * wiggle

            tail_color = (max(20 - tail_factor * i, 0), 255 - tail_factor * i, max(100 - tail_factor * i, 0))
            pygame.draw.circle(self.draw_surf, tail_color, (x, y), ball.radius * (i + 1) / tail_length, 1)
        if ball.hit:
            ball_color = (255 - ball.hit_time, 10*ball.hit_time, 0)
        else:
            ball_color = (20, 255, 90)
        pygame.draw.circle(self.draw_surf, ball_color, (ball.x, ball.y), ball.radius)
        
    
    def draw_paddle(self, paddle):
        paddle_color = (255, 255, 255)
        offset = 0
        if paddle.hit:
            # make paddle warp and bounce when hit
            paddle_color = (255, 0, 0)
            offset = math.sin(paddle.hit_time / 5 * math.pi) * 10
        if paddle.left:
            pygame.draw.rect(self.draw_surf, paddle_color, (paddle.x, paddle.y, paddle.width - offset, paddle.height))
        else:
            pygame.draw.rect(self.draw_surf, paddle_color, (paddle.x + offset, paddle.y, paddle.width - offset, paddle.height))

    def draw_arena(self, arena):
        #print(f"Drawing arena with dirty cells: {arena.dirty_cells}")  # Add this line

        ALIVE_C = (20, 255, 90)
        DEAD_C = (0, 0, 0)
        draw_surf = self.arena_surf
        cell_size = arena.cell_size

        for row, col in arena.dirty_cells:
            color = ALIVE_C if arena.grid[row][col] else DEAD_C
            x = arena.x + col * cell_size[0]
            y = arena.y + row * cell_size[1]
            pygame.draw.ellipse(draw_surf, color, (x, y, cell_size[0], cell_size[1]))

        # Clear the dirty cells list after drawing them
        arena.dirty_cells.clear()

        pygame.draw.rect(draw_surf, ALIVE_C, (arena.x, arena.y, arena.width, arena.height), 2)

    def draw_scorer(self, scorer):
        score_text = f"{scorer.score_left} - {scorer.score_right}"
        text_render = scorer.font.render(score_text, True, (255, 255, 255))
        text_rect = text_render.get_rect(center=(self.width // 2, 20))
        self.draw_surf.blit(text_render, text_rect)

