import pygame
pygame.init()

from gui.text.text_object import TextObject

class TextManager():
    def __init__(self, text_objects: list):
        self.text_objects = text_objects

    def render_text(self, screen) -> None:
        self.__update_texts()
        for _text_obj in self.text_objects:
            screen.blit(_text_obj.render, _text_obj.rect)

    def __update_texts(self) -> None:
        for _text_obj in self.text_objects:
            _text_obj.update_text()