import pygame
pygame.init()

from config.stats import stats

class ObstacleSuper():
    def __init__(self, position: tuple, radius: int, rotation_deg: int):
        self.x, self.y = position
        self.radius = radius
        self.rotation_deg = rotation_deg

        self.selected = False

        self.update_drawing()


    def scale_self(self, change) -> None:
        # min and max sidelength
        if self.radius + change < 5 or self.radius + change > 200: return

        stats.edited = True
        self.radius += change
        self.update_drawing()


    def rotate_self(self, change_deg) -> None:
        """Rotate by certain amount of degrees"""
        stats.edited = True
        self.rotation_deg += change_deg
        self.update_drawing()


    def get_pos(self) -> int:
        return (self.x, self.y)
    

    def get_size(self) -> int:
        return self.radius


    def get_rotation(self) -> int:
        return self.rotation_deg


    def move_by(self, amount: tuple) -> None:
        """Move the obstacle in a direction"""
        stats.edited = True
        
        self.x += amount[0]
        self.y += amount[1]

        self.update_drawing()


    def set_active(self, state: bool) -> None:
        """Sets selected state"""
        self.selected = state
        self.update_drawing()


    def update_drawing(self):
        pass
    
    def check_point_inside(self):
        pass

    def find_normal_at_point(self):
        pass

    def make_json_save(self) -> dict:
        pass

    def load_from_json(self, dict) -> None:
        pass