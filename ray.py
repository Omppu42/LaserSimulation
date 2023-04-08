import math
import pygame
import numpy as np

from obstacles.obstacle_manager import obstacle_manager
from config.stats import stats
from config.settings import settings

pygame.init()

class Ray():
    def __init__(self, start_pos: tuple, screen_size: tuple, dir_deg: float):
        self.x, self.y = start_pos
        self.w, self.h = screen_size
        self.dir_deg = dir_deg
        self.dir_rad = self.dir_deg * math.pi/180

        self.move_vec = (settings.ray_step_size * math.cos(self.dir_rad), settings.ray_step_size * math.sin(self.dir_rad))
        self.rays_surface = pygame.Surface(screen_size)

        self.last_object_hit = None

        pygame.draw.circle(self.rays_surface, (200, 0, 0), (self.x, self.y), 2)

        ROTATION_OFFSET = -90

        dir_arrow = pygame.transform.smoothscale(pygame.image.load("assets/arrow.png"), (64, 64))
        dir_arrow = pygame.transform.rotate(dir_arrow, -self.dir_deg + ROTATION_OFFSET)

        dir_arrow_rect = dir_arrow.get_rect(center=(self.x, self.y))
        self.rays_surface.blit(dir_arrow, dir_arrow_rect)


    def calculate_ray(self) -> None:
        pygame.draw.line(self.rays_surface, (125,0,0), (self.x, self.y), (self.x + self.move_vec[0], self.y + self.move_vec[1]))


    def clear_surface(self) -> None:
        self.rays_surface.fill((0,0,0))


    def update(self) -> None:
        if stats.simulation_running:
            for _ in range(settings.ray_updates_per_frame):

                # Check collisions
                self.check_collisions()
                self.move()

                stats.current_ray_step += 1


    def draw_ray(self, screen: pygame.Surface) -> None:
        screen.blit(self.rays_surface, (0,0))

    def move(self):
        self.x += self.move_vec[0]
        self.y += self.move_vec[1]
        self.calculate_ray()

        stats.ray_pos_rounded = (round(self.x), round(self.y))

    def check_collisions(self) -> None:
        for obs in obstacle_manager.get_obstacles():
            if not obs.check_point_inside((self.x + self.move_vec[0], self.y + self.move_vec[1])): continue

            self.last_object_hit = obs

            # collided
            normalized_normal = obs.find_normal_at_point((self.x, self.y))
            self.calculate_bounce_angle(normalized_normal)
            stats.num_collisions += 1
    

    def calculate_bounce_angle(self, normal: tuple) -> None:
        move_vec_mag = math.sqrt(math.pow(self.x - (self.x + self.move_vec[0]), 2) + math.pow(self.y - (self.y + self.move_vec[1]), 2))
        normalized_move = (self.move_vec[0] / move_vec_mag, self.move_vec[1] / move_vec_mag)

        dot = 2 * np.dot(normalized_move, normal)
        self.move_vec = ((normalized_move[0] - dot * normal[0]) * settings.ray_step_size,
                            (normalized_move[1] - dot * normal[1]) * settings.ray_step_size)