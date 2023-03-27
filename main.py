import pygame
import cProfile

from ray import Ray
from obstacle import SquareObstacle, CircleObstacle

pygame.init()


def main():
    background_colour = (0, 0, 0)
    width, height = 800, 800
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)
    
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Light Reflection Simulation')

    obstacles_square = [SquareObstacle((300, 300), 100, 30), SquareObstacle((600, 150), 100, 60), 
                        SquareObstacle((600, 300), 50, 85), 
                        SquareObstacle((250, 525), 100, 82), SquareObstacle((490, 670), 100, 70), SquareObstacle((600, 480), 100, 70)]

    obstacles_circle = [CircleObstacle(( 440, 250), 51), CircleObstacle(( 450, 180), 50), CircleObstacle(( 400, 500), 20), CircleObstacle(( 600, 360), 20)]

    ray = Ray((width/2, height/2), (width, height), 260)
    ray.calculate_ray()

    running = True

    total_steps = 50000
    current_step = 0

    num_colls = 0

    updates_at_a_time = 10

    while running:
        screen.fill(background_colour)

        if current_step < total_steps:
            for _ in range(updates_at_a_time):
                for obs in obstacles_square:
                    if ray.check_collision_square(obs):
                        num_colls += 1
                        break

                for obs in obstacles_circle:
                    if ray.check_collision_circle(obs):
                        num_colls += 1
                        break

                ray.move()
                current_step += 1

        ray.draw_ray(screen)

        for obs in obstacles_square:
            obs.draw(screen)
        for obs in obstacles_circle:
            obs.draw(screen)
            

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        fps = font.render(str(round(clock.get_fps())), True, (255, 0, 0))
        screen.blit(fps, (10,10))

        pygame.display.update()
        clock.tick(60)

    

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