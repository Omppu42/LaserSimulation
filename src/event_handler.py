import pygame, sys, json
pygame.init()

from gui.sidebar import Sidebar
from gui.unsaved_changes import UnsavedChangesDialog

from obstacles.obstacle_manager import obstacle_manager
from config.stats import stats
from ray import Ray


def handle_events(sidebar: Sidebar, ray: Ray, clock: pygame.time.Clock) -> None:
    stats.fps = round(clock.get_fps())
    obstacle_manager.check_keys_held()
    ray.check_keys()
    
    for event in pygame.event.get():
        ray.handle_event(event)

        if event.type == pygame.QUIT:
            on_exit(sidebar)

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


def on_exit(sidebar) -> None:
    if stats.edited:
        UnsavedChangesDialog("You have unsaved changes.\n Save before exiting?", sidebar)

    with open("src/config/last_session.json", "w") as f:
        data = {}
        data["last_save"] = stats.current_scene

        json.dump(data, f, indent=2)

    sys.exit()