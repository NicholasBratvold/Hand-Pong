import pygame

class Scorer:
    def __init__(self, font_size=36):
        self.font = pygame.font.SysFont(None, font_size)
        self.score_left = 0
        self.score_right = 0

    def draw(self, screen, width):
        score_text = f"{self.score_left} - {self.score_right}"
        text_render = self.font.render(score_text, True, (255, 255, 255))
        text_rect = text_render.get_rect(center=(width // 2, 20))
        screen.blit(text_render, text_rect)