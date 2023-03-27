import math
import pygame

import numpy as np

from obstacle import SquareObstacle, CircleObstacle
pygame.init()

class Ray():
    def __init__(self, start_pos: tuple, screen_size: tuple, dir_deg: float):
        self.x, self.y = start_pos
        self.w, self.h = screen_size
        self.dir_deg = dir_deg
        self.dir_rad = self.dir_deg * math.pi/180
        self.step_size = .5
        self.hit_between_points = None # tuple
        self.hit_circle_center_at_pos = None # tuple

        self.move_vec = (self.step_size * math.cos(self.dir_rad), self.step_size * math.sin(self.dir_rad))
        self.rays_surface = pygame.Surface(screen_size)
    
        pygame.draw.circle(self.rays_surface, (255,255,255), (self.x, self.y), 1)


    def calculate_ray(self) -> None:
        pygame.draw.line(self.rays_surface, (255,0,0), (self.x, self.y), (self.x + self.move_vec[0], self.y + self.move_vec[1]))


    def draw_ray(self, screen: pygame.Surface) -> None:
        screen.blit(self.rays_surface, (0,0))

    def move(self):
        self.x += self.move_vec[0]
        self.y += self.move_vec[1]
        self.calculate_ray()

    def check_collision_square(self, obstacle: SquareObstacle) -> bool:
        hit_between_points = obstacle.check_point_on_edge((self.x, self.y), self.hit_between_points)
        if hit_between_points == None: return False

        self.hit_between_points = hit_between_points

        # collided
        normalized_normal_vec = obstacle.find_normal_at_point((self.x, self.y))

        move_vec_mag = math.sqrt(math.pow(self.x - (self.x + self.move_vec[0]), 2) + math.pow(self.y - (self.y + self.move_vec[1]), 2))

        normalized_move = (self.move_vec[0] / move_vec_mag, self.move_vec[1] / move_vec_mag)

        dot = 2 * np.dot(normalized_move, normalized_normal_vec)
        self.move_vec = ((normalized_move[0] - dot * normalized_normal_vec[0]) * self.step_size,
                            (normalized_move[1] - dot * normalized_normal_vec[1]) * self.step_size)
        return True
    

    def check_collision_circle(self, obstacle: CircleObstacle) -> bool:
        collision = obstacle.check_collision((self.x, self.y), (0,0))
        if collision:
            self.hit_circle_center_at_pos = collision
            self.hit_between_points = (0, 0)
        else: return False

        # collided
        normalized_normal = obstacle.find_normal_at_point((self.x, self.y))

        move_vec_mag = math.sqrt(math.pow(self.x - (self.x + self.move_vec[0]), 2) + math.pow(self.y - (self.y + self.move_vec[1]), 2))

        normalized_move = (self.move_vec[0] / move_vec_mag, self.move_vec[1] / move_vec_mag)

        dot = 2 * np.dot(normalized_move, normalized_normal)
        self.move_vec = ((normalized_move[0] - dot * normalized_normal[0]) * self.step_size,
                            (normalized_move[1] - dot * normalized_normal[1]) * self.step_size)
        return True