import math
import pygame
pygame.init()

class CircleObstacle():
    def __init__(self, center_pos: tuple, radius: float):
        self.x, self.y = center_pos
        self.radius = radius

        self.surf = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA, 32)
        self.surf = self.surf.convert_alpha()
        self.surf.fill((0, 0, 0, 0))
        
        self.width = 1
        self.selected = False

        self.__redraw_surf()
        
    
    def __repr__(self) -> str:
        return f"Circle Obstacle at pos: ({self.x}, {self.y}) radius: {self.radius}"


    def __redraw_surf(self) -> None:
        col = (250, 250, 250, 255) if self.selected else (180, 180, 180, 255)
        pygame.draw.circle(self.surf, col, (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.surf, (0, 0, 0, 0), (self.radius, self.radius), self.radius - self.width)
        self.rect = self.surf.get_rect(center=(self.x, self.y))


    def move_by(self, amount: tuple) -> None:
        """Move the whole square in a direction"""
        self.x += amount[0]
        self.y += amount[1]

        self.__redraw_surf()


    def set_active(self, state: bool) -> None:
        """Sets selected state"""
        self.selected = state
        self.__redraw_surf()



    def draw(self, screen: pygame.Surface):
        screen.blit(self.surf, self.rect)


    def check_clicked(self, point) -> bool:
        dist_to_center = math.sqrt( math.pow(self.x - point[0], 2) + math.pow(self.y - point[1], 2) )
        return dist_to_center < self.radius
    

    def check_point_inside(self, point: tuple) -> bool:
        """If point inside circle"""
        dist_to_center = math.sqrt( math.pow(self.x - point[0], 2) + math.pow(self.y - point[1], 2) )

        if dist_to_center < self.radius:
            return True

        return False
            
    
    def find_normal_at_point(self, point: tuple) -> tuple:
        # offset point onto the edge of the circle
        mag = math.sqrt( math.pow(point[0] - self.x, 2) + math.pow(point[1] - self.y, 2) )

        Cx = self.x + self.radius * ( (point[0] - self.x) / mag )
        Cy = self.y + self.radius * ( (point[1] - self.y) / mag )

        normal = (Cx - self.x, Cy - self.y)

        length = math.sqrt( math.pow(normal[0], 2) + math.pow(normal[1], 2) )
        normal = (normal[0] / length, normal[1] / length)

        return normal