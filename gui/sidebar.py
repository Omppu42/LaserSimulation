import pygame

from gui.button import Button
from obstacles.manager import obstacle_manager
from config.stats import stats

pygame.init()

class Sidebar():
    def __init__(self, pos: tuple, size: tuple) -> None:
        self.x, self.y = pos
        self.w, self.h = size

        self.selected_index = -1

        self.surf = pygame.Surface((self.w, self.h))
        self.surf.fill((10, 10, 10))

        self.play_button = Button(self.x + self.w / 2, self.h - 50, 200, 50, text="Start", font_size=32)
        self.font = pygame.font.Font(None, 32)
        self.x_to_delete_render = self.font.render("Press X to delete", True, (100, 100, 100))
        self.x_to_delete_rect = self.x_to_delete_render.get_rect(center=(self.x + self.w / 2, self.h - 100))

    def draw(self, screen) -> None:
        screen.blit(self.surf, (self.x, self.y))

        if obstacle_manager.selected_index != -1:
            screen.blit(self.x_to_delete_render, self.x_to_delete_rect)

        if not stats.updating_ray:
            self.play_button.draw(screen)


    def check_mouse_motion(self):
        self.play_button.check_hover(pygame.mouse.get_pos())

    def check_click(self):
        if self.play_button.check_click():
            stats.updating_ray = not stats.updating_ray