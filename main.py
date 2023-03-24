import pygame

from ray import Ray
from obstacle import SquareObstacle

pygame.init()


def main():
    background_colour = (0, 0, 0)
    width, height = 800, 800
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)
    
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Light Reflection Simulation')

    obstacles_square = [SquareObstacle((300, 300), 100, 30), SquareObstacle((600, 150), 100, 60), SquareObstacle((500, 350), 50, 60), 
                        SquareObstacle((400, 100), 10, 84), SquareObstacle((300, 10), 10, 82)]

    ray = Ray((width/2, height/2), (width, height), 260)
    ray.calculate_ray()

    running = True

    total_steps = 2000
    current_step = 0

    collision_cooldown_frames = 5
    collision_cooldown_current = 0
    on_collision_cooldown = False
    num_colls = 0

    while running:
        screen.fill(background_colour)

        # FIXME: If hits a corner, just passes through it

        # ray creation loop
        # if num_colls == 3:
        #     current_step = 101
        if current_step < total_steps:
            for obs in obstacles_square:

                # collision cooldown
                if on_collision_cooldown and collision_cooldown_current < collision_cooldown_frames: 
                    collision_cooldown_current += 1
                    break

                on_collision_cooldown = False

                if ray.check_collision_square(obs):
                    on_collision_cooldown = True
                    num_colls += 1
                    break


            ray.move()
            current_step += 1

        ray.draw_ray(screen)

        for obs in obstacles_square:
            obs.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        fps = font.render(str(round(clock.get_fps())), True, (255, 0, 0))
        screen.blit(fps, (10,10))

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()