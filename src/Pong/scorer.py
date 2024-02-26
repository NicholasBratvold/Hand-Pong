import pygame

class Scorer:
    def __init__(self, font_size=36):
        self.font = pygame.font.SysFont(None, font_size)
        self.score_left = 0
        self.score_right = 0
