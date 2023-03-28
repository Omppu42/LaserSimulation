import pygame
from obstacle import CircleObstacle, SquareObstacle


pygame.init()

class Sidebar():
    def __init__(self, pos: tuple, size: tuple, screen: pygame.Surface, square_obtacles: list[SquareObstacle], circle_obstacles: list[CircleObstacle]) -> None:
        self.x, self.y = pos
        self.w, self.h = size
        self.screen = screen
        self.square_obtacles = square_obtacles
        self.circle_obstacles = circle_obstacles

        self.square_obtacles.sort(key=lambda x: x.side_length)
        self.circle_obstacles.sort(key=lambda x: x.radius)

        self.all_obstacles = self.circle_obstacles + self.square_obtacles
        self.selected_index = -1

        self.surf = pygame.Surface((self.w, self.h))
        self.surf.fill((10, 10, 10))

    def draw(self) -> None:
        self.screen.blit(self.surf, (self.x, self.y))
        # TODO: Draw configuration settings when needed to configure the objects


    def check_click(self, mouse_pos: tuple) -> None:
        for index, ostacle in enumerate(self.all_obstacles):
            # already selected
            if index == self.selected_index: continue

            # check if clicked
            if ostacle.check_clicked(mouse_pos):
                self.selected_index = self.all_obstacles.index(ostacle)
                break
        else:
            # didn't click any
            self.selected_index = -1
        
        # update selected status
        for index, obstacle in enumerate(self.all_obstacles):
            if index == self.selected_index:
                obstacle.set_active(True)
            else:
                obstacle.set_active(False)    