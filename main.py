import cProfile, os
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

    #TODO: Before starting add number text field to type max fps, updates at a time, max steps before stopping

    clock = pygame.time.Clock()

    sidebar = Sidebar((settings.screen_width - settings.sidebar_width, 0), 
                      (settings.sidebar_width, settings.screen_height))
    
    ray = Ray((400, 400), (settings.screen_width - settings.sidebar_width, settings.screen_height), 260)
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