import pygame
pygame.init()

class Text_Object():
    def __init__(self, text: str, center_pos_xy: tuple, font: pygame.font.Font):
        self.render = font.render(text, True, (100, 100, 100))
        self.rect = self.render.get_rect(center=(center_pos_xy))