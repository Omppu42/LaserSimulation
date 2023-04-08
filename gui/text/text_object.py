import pygame
pygame.init()

class TextObject():
    def __init__(self, text: str, center_pos_xy: tuple, font: pygame.font.Font):
        """Creates a text render and a rect for it \n 
        Any placeholder values need to be updated with set_placeholder() function"""
        self.__text = text
        self.__font = font
        self.__center_pos = center_pos_xy

        self.render = self.__font.render(self.__text, True, (100, 100, 100))
        self.rect = self.render.get_rect(center=(self.__center_pos))


    def set_placeholder(self, placeholder) -> None:
        self.render = self.__font.render(self.__text % placeholder, True, (100, 100, 100))
        self.rect = self.render.get_rect(center=(self.__center_pos))