import pygame

from gui.button import Button
from gui.text.text_object import Text_Object
from gui.text.text_group import Text_Group

from obstacles.manager import obstacle_manager

from config.stats import stats
from config.settings import settings

pygame.init()


class Sidebar():
    def __init__(self, pos: tuple, size: tuple) -> None:
        self.x, self.y = pos
        self.w, self.h = size

        self.selected_index = -1

        self.surf = pygame.Surface((self.w, self.h))
        self.surf.fill((10, 10, 10))

        button_font = pygame.font.Font(settings.global_font_path, 26)
        self.play_button = Button(self.x + self.w / 2, self.h - 50, 200, 50, text="Start Simulation", font=button_font)

        self.init_texts()


    def init_texts(self) -> None:
        font = pygame.font.Font(settings.global_font_path, 20)

        self.obstacle_selected_texts = Text_Group( [Text_Object("Arrows to Rotate and Scale", (self.x + self.w / 2, self.h - 130), font),
                                                    Text_Object("'x' to Delete", (self.x + self.w / 2, self.h - 100), font)] )

        self.no_obstacle_selected_texts = Text_Group( [Text_Object("Select an obstacle to Modify it", (self.x + self.w / 2, self.h - 115), font)] )


    def draw(self, screen) -> None:
        screen.blit(self.surf, (self.x, self.y))

        if not stats.updating_ray:
            self.render_texts(screen)
            self.play_button.draw(screen)


    def render_texts(self, screen) -> None:
        if obstacle_manager.selected_index == -1:
            self.no_obstacle_selected_texts.render_text(screen)

        else:
            self.obstacle_selected_texts.render_text(screen)


    def check_mouse_motion(self):
        if stats.updating_ray == True: return

        self.play_button.check_hover(pygame.mouse.get_pos())

    def check_click_play_button(self) -> bool:
        if stats.updating_ray == True: return False

        if self.play_button.check_click():
            stats.updating_ray = True
            return True
        
        return False