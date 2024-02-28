import pygame
from Pong.components import Ball, Arena, Paddle, Scorer
import math

class Animation:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.draw_surf = pygame.Surface((self.width, self.height))
        pygame.display.set_caption("Pong")


    def draw(self, components):
        self.draw_surf.fill((0,0,0,255))
        for component in components:
            self.draw_component(component)
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
    
    def resize(self, w, h, components):
        width_ratio = w / self.width
        height_ratio = h / self.height
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        for component in components: 
            component.resize(width_ratio, height_ratio)


    def draw_ball(self, ball):
        # Draw the tail circles with changing colors
        tail_length = len(ball.tail_positions)
        tail_factor = 255 // tail_length
        for i, (x, y) in enumerate(ball.tail_positions):
            if i >= tail_length:
                break
            tail_color = (255, 255 - tail_factor * i, 255 - i, 255 - tail_factor * i)
            pygame.draw.circle(self.draw_surf, tail_color, (x, y), ball.radius * (tail_length - i) / tail_length)

        ball_color = (255, 255, 255)
        pygame.draw.circle(self.draw_surf, ball_color, (ball.x, ball.y), ball.radius)
        
    
    def draw_paddle(self, paddle):
        pygame.draw.rect(self.draw_surf, (255, 255, 255), (paddle.x, paddle.y, paddle.width, paddle.height))

    def draw_arena(self, arena):

        ALIVE_C = (161, 98, 168)
        DEAD_C = (0, 0, 0)
    # Calculate the starting point of the grid
        
        for row in range(arena.rows):
            for col in range(arena.cols):
                color = ALIVE_C if arena.grid[row][col] else DEAD_C
                pygame.draw.rect(self.draw_surf, color, 
                                (arena.x + col * arena.cell_size[0], 
                                arena.y + row * arena.cell_size[1], 
                                arena.cell_size[0], 
                                arena.cell_size[1]))
        pygame.draw.rect(self.draw_surf, ALIVE_C, (arena.x, arena.y, arena.width, arena.height), 2)
        pygame.draw.rect(self.draw_surf, (255,255,255), (arena.x, arena.y, arena.cell_size[0]*arena.cols, arena.cell_size[1]*arena.rows), 2)
    
    def draw_scorer(self, scorer):
        score_text = f"{scorer.score_left} - {scorer.score_right}"
        text_render = scorer.font.render(score_text, True, (255, 255, 255))
        text_rect = text_render.get_rect(center=(self.width // 2, 20))
        self.draw_surf.blit(text_render, text_rect)

