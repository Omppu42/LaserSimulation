import math
import pygame

import numpy as np
from obstacle_square import SquareObstacle
from obstacle_circle import CircleObstacle
pygame.init()

class Ray():
    def __init__(self, start_pos: tuple, screen_size: tuple, dir_deg: float):
        self.x, self.y = start_pos
        self.w, self.h = screen_size
        self.dir_deg = dir_deg
        self.dir_rad = self.dir_deg * math.pi/180
        self.step_size = .5

        self.move_vec = (self.step_size * math.cos(self.dir_rad), self.step_size * math.sin(self.dir_rad))
        self.rays_surface = pygame.Surface(screen_size)

        self.last_object_hit = None
    
        pygame.draw.circle(self.rays_surface, (255,255,255), (self.x, self.y), 1)


    def calculate_ray(self) -> None:
        pygame.draw.line(self.rays_surface, (125,0,0), (self.x, self.y), (self.x + self.move_vec[0], self.y + self.move_vec[1]))


    def draw_ray(self, screen: pygame.Surface) -> None:
        screen.blit(self.rays_surface, (0,0))

    def move(self):
        self.x += self.move_vec[0]
        self.y += self.move_vec[1]
        self.calculate_ray()

    def check_collision(self, obstacle: SquareObstacle | CircleObstacle) -> bool:
        # hit_between_points = obstacle.check_point_on_edge((self.x, self.y), self.hit_between_points)
        # if hit_between_points == None: return False

        # self.hit_between_points = hit_between_points

        #if obstacle == self.last_object_hit: return

        if not obstacle.check_point_inside((self.x + self.move_vec[0], self.y + self.move_vec[1])): return

        self.last_object_hit = obstacle

        # collided
        normalized_normal = obstacle.find_normal_at_point((self.x, self.y))
        self.calculate_bounce_angle(normalized_normal)
        return True
    

    def calculate_bounce_angle(self, normal: tuple) -> None:
        move_vec_mag = math.sqrt(math.pow(self.x - (self.x + self.move_vec[0]), 2) + math.pow(self.y - (self.y + self.move_vec[1]), 2))
        normalized_move = (self.move_vec[0] / move_vec_mag, self.move_vec[1] / move_vec_mag)

        dot = 2 * np.dot(normalized_move, normal)
        self.move_vec = ((normalized_move[0] - dot * normal[0]) * self.step_size,
                            (normalized_move[1] - dot * normal[1]) * self.step_size)