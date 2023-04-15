import cProfile, os, sys

if os.path.basename(os.getcwd()) == "src":
    os.chdir(os.path.abspath("../"))

ver = sys.version_info
if ver.major != 3  or ver.minor > 10:
    raise Exception("Please use Python 3.9 - 3.10. Python version 3.11 isn't supported")

if ver.major == 3 and ver.minor < 9:
    print("CAUTION: The program is supposed to be run with Python version 3.9. Going bellow this there might be some bugs.")

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame
pygame.init()

def main():
    from config.settings import settings
    from config.stats import stats

    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption('Lazer Simulation')

    from ray import Ray
    from gui.sidebar import Sidebar
    from obstacles.obstacle_manager import obstacle_manager
    from event_handler import handle_events

    #TODO: Ctrl + S to save

    clock = pygame.time.Clock()

    ray = Ray((500, 250), (settings.screen_width - settings.sidebar_width, settings.screen_height), 260)

    sidebar = Sidebar((settings.screen_width - settings.sidebar_width, 0), 
                      (settings.sidebar_width, settings.screen_height), ray, screen)
    
    ray.calculate_ray()

    while True:
        screen.fill(settings.bg_color)

        # Move ray
        ray.update()

        # Draw
        ray.draw_ray(screen)
        obstacle_manager.draw_obstacles(screen)
        sidebar.draw(screen)

        # Pygame Events
        handle_events(sidebar, ray, clock)

        pygame.display.update()

        if stats.simulation_running:
            # Clicked start button
            clock.tick(settings.max_fps)
        else:
            # Config mode
            clock.tick(settings.start_fps_limit)


if __name__ == "__main__":
    from config.settings import settings

    if settings.profile:
        pr = cProfile.Profile()
        pr.enable()

        main()

        pr.disable()
        pr.print_stats()
    else:
        main()