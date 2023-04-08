import pygame
pygame.init()

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

        self.radius += change
        self.update_drawing()


    def rotate_self(self, change_deg) -> None:
        """Rotate by certain amount of degrees"""
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
        self.x += amount[0]
        self.y += amount[1]

        self.update_drawing()


    def set_active(self, state: bool) -> None:
        """Sets selected state"""
        self.selected = state
        self.update_drawing()


    def update_drawing(self):
        raise NotImplementedError("Not implemented")