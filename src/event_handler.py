import pygame, sys, json
pygame.init()

from gui.sidebar import Sidebar
from gui.tkinter.unsaved_changes import UnsavedChangesDialog

from obstacles.obstacle_manager import obstacle_manager
from config.stats import stats
from config.settings import settings

from ray import Ray


def handle_events(sidebar: Sidebar, ray: Ray, clock: pygame.time.Clock, profiler) -> None:
    stats.fps = round(clock.get_fps())
    obstacle_manager.check_keys_held()
    ray.check_keys()
    
    for event in pygame.event.get():
        ray.handle_event(event)

        if event.type == pygame.QUIT:
            on_exit(sidebar, profiler)

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

    # handle tkinter window opening events that need to wait for some time before openign
    if stats.tkinter_func_to_run[1] == 20:
        stats.tkinter_func_to_run[0]()

    if not stats.tkinter_func_to_run[0] is None:
        stats.tkinter_func_to_run = (stats.tkinter_func_to_run[0], stats.tkinter_func_to_run[1] + 1)


def on_exit(sidebar, profiler) -> None:
    if stats.edited:
        UnsavedChangesDialog("You have unsaved changes.\n Save before exiting?", sidebar)

    with open("src/config/last_session.json", "w") as f:
        data = {}
        data["last_save"] = stats.current_scene

        json.dump(data, f, indent=2)

    if settings.profile:
        profiler.disable()
        profiler.print_stats()

    sys.exit()