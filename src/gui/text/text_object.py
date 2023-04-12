import pygame
pygame.init()

from config.stats import stats

class TextObject():
    def __init__(self, text: str, center_pos_xy: tuple, font: pygame.font.Font, placeholder_key=""):
        """Creates a text render and a rect for it \n 
        If placeholders exist, add the key of stats.sidebar_texts_data that has the value.
        If no placeholder key is given, the placeholder will never be filled"""
        self.__text = text
        self.__font = font
        self.__center_pos = center_pos_xy
        self.__placeholder_key = placeholder_key

        self.render = self.__font.render(self.__text, True, (100, 100, 100))
        self.rect = self.render.get_rect(center=(self.__center_pos))

        self.update_text()

    def update_text(self) -> None:
        if self.__placeholder_key == "": return
        
        self.render = self.__font.render(self.__text % stats.sidebar_texts_data[self.__placeholder_key], True, (100, 100, 100))
        self.rect = self.render.get_rect(center=(self.__center_pos))