import pygame
import cProfile

from ray import Ray
from obstacle import SquareObstacle, CircleObstacle
from sidebar import Sidebar

pygame.init()

#TODO: To improve performance, detect square collision with check_clicked() instead of check_point_on_edge(). That way the laser can never be inside, but we don't need that

def main():
    background_colour = (0, 0, 0)
    width, height = 1100, 800
    sidebar_width = 300

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 32)
    
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Lazer Simulation')

    obstacles_square = [SquareObstacle((300, 300), 100, 30), SquareObstacle((600, 150), 100, 60), 
                        SquareObstacle((600, 300), 50, 85), 
                        SquareObstacle((250, 525), 100, 82), SquareObstacle((490, 670), 100, 70), SquareObstacle((600, 480), 100, 70)]

    obstacles_circle = [CircleObstacle(( 440, 250), 52), CircleObstacle(( 450, 180), 50), CircleObstacle(( 400, 500), 20), CircleObstacle(( 600, 360), 20)]

    sidebar = Sidebar((width - sidebar_width, 0), (sidebar_width, height), screen, obstacles_square, obstacles_circle)
    ray = Ray((400, 400), (width - sidebar_width, height), 260)
    ray.calculate_ray()

    running = True

    total_steps = 500000
    current_step = 0

    num_colls = 0

    updates_at_a_time = 50

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
            
        sidebar.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    sidebar.check_click(pygame.mouse.get_pos())
                    


        fps = font.render(str(round(clock.get_fps())), True, (255, 0, 0))
        screen.blit(fps, (10,10))

        pygame.display.update()
        clock.tick(600)

    

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