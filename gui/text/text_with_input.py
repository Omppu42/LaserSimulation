import pygame
pygame.init()

from gui.input_field import NumberInputField
from config.settings import settings

class TextWithInputObject():
    __INPUTFIELD_SIZE = (64, 32)

    def __init__(self, text: str, text_pos_x: int, y_pos: int, default_value: float, max_chars: int, font: pygame.font.Font, empty_field_value="0", int_only=False):
        """Creates a text render and a rect for it \n 
        Any placeholder values need to be updated with set_placeholder() function"""
        self.__text = text
        self.__font = font
        self.__text_pos = (text_pos_x, y_pos)

        self.__input_field_pos = (text_pos_x + 170, y_pos)

        self.text_render = self.__font.render(self.__text, True, (100, 100, 100))
        self.text_rect = self.text_render.get_rect(midleft=self.__text_pos)
        
        font = pygame.font.Font(settings.global_font_path, 20) 
        
        self.input_field = NumberInputField((self.__input_field_pos[0], self.__input_field_pos[1] - TextWithInputObject.__INPUTFIELD_SIZE[1] / 2), 
                                            self.__INPUTFIELD_SIZE, font, max_chars, default_value, empty=str(empty_field_value), int_only=int_only)


    def set_placeholder(self, placeholder) -> None:
        self.text_render = self.__font.render(self.__text % placeholder, True, (100, 100, 100))
        self.text_rect = self.text_render.get_rect(topleft=self.__text_pos)

    
    def draw(self, screen) -> None:
        screen.blit(self.text_render, self.text_rect)
        self.input_field.draw(screen)