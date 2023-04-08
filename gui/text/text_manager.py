import pygame
pygame.init()

from gui.text.text_object import TextObject

class TextManager():
    def __init__(self, text_objects: list[TextObject]):
        self.text_objects = text_objects

    def render_text(self, screen) -> None:
        for _text_obj in self.text_objects:
            screen.blit(_text_obj.render, _text_obj.rect)