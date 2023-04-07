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
    from obstacles.manager import obstacle_manager

    #TODO: Make sidebar into a debug window: show xy, number of collisions, fps
    #TODO: Before starting add number text field to type max fps, updates at a time, max steps before stopping
    #TODO: Add buttons for spawning sqares and circles

    clock = pygame.time.Clock()
    font = pygame.font.Font(settings.global_font_path, 24)

    sidebar = Sidebar((settings.screen_width - settings.sidebar_width, 0), 
                      (settings.sidebar_width, settings.screen_height))
    
    ray = Ray((400, 400), (settings.screen_width - settings.sidebar_width, settings.screen_height), 260)
    ray.calculate_ray()

    running = True
    while running:
        screen.fill(settings.bg_color)

        # Move ray
        if stats.updating_ray and stats.current_ray_step < settings.total_steps:
            for _ in range(settings.ray_updates_per_frame):

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
        obstacle_manager.check_keys_held()

        for event in pygame.event.get():
            obstacle_manager.handle_events(event)
            
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                obstacle_manager.check_mouse_up()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:    
                    obstacle_manager.check_click(pygame.mouse.get_pos())
                    if sidebar.check_click_play_button():
                        ray.clear_surface()

            if event.type == pygame.MOUSEMOTION:
                sidebar.check_mouse_motion()
                obstacle_manager.mouse_motion()


        pygame.display.update()

        if stats.updating_ray:
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