import pygame, sys
pygame.init()

from gui.sidebar import Sidebar
from obstacles.obstacle_manager import obstacle_manager
from config.stats import stats
from ray import Ray


def handle_events(sidebar: Sidebar, ray: Ray, clock: pygame.time.Clock) -> None:
    stats.fps = round(clock.get_fps())
    obstacle_manager.check_keys_held()

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            sidebar.handle_key_pressed(event)
            obstacle_manager.handle_events(event)

        if event.type == pygame.MOUSEBUTTONUP:
            obstacle_manager.check_mouse_up()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:    
                obstacle_manager.check_click(pygame.mouse.get_pos())
                sidebar.check_click(ray)

        if event.type == pygame.MOUSEMOTION:
            sidebar.check_mouse_motion()
            obstacle_manager.mouse_motion()