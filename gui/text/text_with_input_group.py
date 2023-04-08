import pygame
pygame.init()

from gui.text.text_with_input import TextWithInputObject
from gui.input_field import NumberInputField

class TextWithInputGroup():
    def __init__(self, objects: list[TextWithInputObject]):
        self.objects = objects

    def check_click(self) -> None:
        for _obj in self.objects:
            _obj.input_field.check_click()

    def on_keydown(self, event: pygame.event.Event) -> None:
        for _obj in self.objects:
            _obj.input_field.on_keydown(event)

    def draw(self, screen) -> None:
        for _obj in self.objects:
            _obj.draw(screen)

    def get_inputfield_at_index(self, index: int) -> NumberInputField:
        return self.objects[index].input_field
    
    def fix_strings(self) -> None:
        for _obj in self.objects:
            _obj.input_field.fix_text()