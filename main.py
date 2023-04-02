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
    from sidebar import Sidebar
    from obstacles.manager import obstacle_manager

    #TODO: Press 'x' to delete the obstacle when selected
    #TODO: Make sidebar into a debug window: show xy, number of collisions, fps
    #TODO: Before starting add number text field to type max fps, updates at a time, max steps before stopping
    #TODO: Add buttons for spawning sqares and circles

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)

    sidebar = Sidebar((settings.screen_width - settings.sidebar_width, 0), 
                      (settings.sidebar_width, settings.screen_height))
    
    ray = Ray((400, 400), (settings.screen_width - settings.sidebar_width, settings.screen_height), 260)
    ray.calculate_ray()

    running = True
    while running:
        screen.fill(settings.bg_color)

        # Move ray
        if sidebar.update_ray and stats.current_ray_step < settings.total_steps:
            for _ in range(settings.updates_at_a_time):

                # Check collisions
                ray.check_collisions()
                ray.move()

                stats.current_ray_step += 1

        # Draw
        ray.draw_ray(screen)        
        obstacle_manager.draw_obstacles(screen)
        sidebar.draw(screen)

        fps = font.render(str(round(clock.get_fps())), True, (255, 0, 0))
        screen.blit(fps, (10,10))

        # Pygame Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                sidebar.check_mouse_up()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    sidebar.check_click(pygame.mouse.get_pos())

            if event.type == pygame.MOUSEMOTION:
                sidebar.mouse_motion(event)


        pygame.display.update()
        clock.tick(settings.max_fps)


if __name__ == "__main__":
    profile = False

    if profile:
        pr = cProfile.Profile()
        pr.enable()

        main()

        pr.disable()
        pr.print_stats()
    else:
        main()