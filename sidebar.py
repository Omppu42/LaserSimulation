import pygame

from obstacles.manager import obstacle_manager
from button import Button

pygame.init()

class Sidebar():
    def __init__(self, pos: tuple, size: tuple, screen: pygame.Surface) -> None:
        self.x, self.y = pos
        self.w, self.h = size
        self.screen = screen

        self.selected_index = -1

        self.surf = pygame.Surface((self.w, self.h))
        self.surf.fill((10, 10, 10))

        self.play_button = Button(self.x + self.w / 2, self.h - 50, 200, 50, text="Start", font_size=32)
        self.update_ray = False

    def draw(self) -> None:
        self.screen.blit(self.surf, (self.x, self.y))
        
        if not self.update_ray:
            self.play_button.draw(self.screen)


    def mouse_motion(self, event) -> None:
        if self.update_ray: return

        self.play_button.check_hover(pygame.mouse.get_pos())
        
        if pygame.mouse.get_pressed()[0]:
            if self.selected_index != -1:
                
                mouse_moved = pygame.mouse.get_rel()
                obstacle_manager.get_obstacles()[self.selected_index].move_by(mouse_moved)


    def check_mouse_up(self) -> None:
        self.selected_index = -1
        self.update_obstacle_status()

    def check_click(self, mouse_pos: tuple) -> None:
        if self.update_ray: return

        pygame.mouse.get_rel()

        if self.play_button.check_click():
            self.update_ray = not self.update_ray

        for index, ostacle in enumerate(obstacle_manager.get_obstacles()):
            # already selected
            if index == self.selected_index: continue

            # check if clicked
            if ostacle.check_point_inside(mouse_pos):
                self.selected_index = obstacle_manager.get_obstacles().index(ostacle)
                break
        else:
            # didn't click any
            self.selected_index = -1

        self.update_obstacle_status()


    def update_obstacle_status(self):
        # update selected status
        for index, obstacle in enumerate(obstacle_manager.get_obstacles()):
            if index == self.selected_index:
                obstacle.set_active(True)
            else:
                obstacle.set_active(False)    