import pygame, os, json
pygame.init()

from obstacles.square import SquareObstacle
from obstacles.circle import CircleObstacle
from obstacles.obstacle import ObstacleSuper

from config.stats import stats
from config.settings import settings

class ObstacleManager():
    def __init__(self) -> None:
        self.__obstacles_square = [ SquareObstacle((300, 300), 100, 30), SquareObstacle((600, 150), 100, 60), 
                                    SquareObstacle((600, 300), 50, 85), SquareObstacle((500, 480), 40, 20),
                                    SquareObstacle((250, 525), 100, 82), SquareObstacle((475, 675), 100, 70), SquareObstacle((600, 480), 100, 70),
                                    SquareObstacle((500, 400), 100, 100)]

        self.__obstacles_circle = [CircleObstacle(( 440, 250), 46), CircleObstacle(( 450, 180), 50), CircleObstacle(( 400, 500), 20), CircleObstacle(( 600, 360), 20)]
        
        self.__obstacles_square.sort(key=lambda x: x.radius)
        self.__obstacles_circle.sort(key=lambda x: x.radius)

        self.__all_obstacles = self.__obstacles_circle + self.__obstacles_square
        self.selected_index = -1


    def load_from_json(self, dict) -> None:
        self.__obstacles_square = []
        self.__obstacles_circle = []

        for _square in dict["squares"]:
            self.__obstacles_square.append( SquareObstacle( (_square["position"]["x"], _square["position"]["y"]),
                                                             _square["scale"], _square["rotation"]) )

        for _circle in dict["circles"]:
            self.__obstacles_square.append( CircleObstacle((_circle["position"]["x"], _circle["position"]["y"]),
                                                            _circle["scale"]) )

        self.__obstacles_square.sort(key=lambda x: x.radius)
        self.__obstacles_circle.sort(key=lambda x: x.radius)

        self.__all_obstacles = self.__obstacles_circle + self.__obstacles_square
        self.selected_index = -1

    def get_obstacles(self) -> list[ObstacleSuper]:
        return self.__all_obstacles

    def get_selected_obstacle(self) -> ObstacleSuper:
        return self.__all_obstacles[self.selected_index]
    

    def draw_obstacles(self, screen) -> None:
        for obs in self.__all_obstacles:
            obs.draw(screen)


    def handle_events(self, event) -> None:
        if self.selected_index == -1: return

        if event.key == pygame.K_x:
            stats.edited = True
            self.__all_obstacles.pop(self.selected_index)
            self.selected_index = -1


    def check_keys_held(self) -> None:
        if self.selected_index == -1: return

        keys = pygame.key.get_pressed()
        obs = self.__all_obstacles[self.selected_index]
        
        #Scale
        if keys[pygame.K_UP]: 
            obs.scale_self(1)
        if keys[pygame.K_DOWN]:
            obs.scale_self(-1)

        #Rotate
        if keys[pygame.K_LEFT]:
            obs.rotate_self(-1)
        if keys[pygame.K_RIGHT]:  
            obs.rotate_self(1)
            
    
    def spawn_square(self) -> None:
        self.__all_obstacles.append(SquareObstacle((400, 400), 50, 0))

    def spawn_circle(self) -> None:
        self.__all_obstacles.append(CircleObstacle((400, 400), 50))

    
    def mouse_motion(self) -> None:
        if stats.simulation_running: return
        
        if pygame.mouse.get_pressed()[0]:
            if self.selected_index != -1:
                mouse_moved = pygame.mouse.get_rel()

                _selected_obs = self.get_obstacles()[self.selected_index]
                _selected_obs.move_by(mouse_moved)


    def check_mouse_up(self) -> None:
        self.selected_index = -1
        self.update_obstacles_status()


    def check_click(self, mouse_pos: tuple) -> None:
        if stats.simulation_running or stats.ray_selected: return

        pygame.mouse.get_rel()

        for _index, _ostacle in enumerate(self.get_obstacles()):
            # already selected
            if _index == self.selected_index: continue

            if _ostacle.check_point_inside(mouse_pos):
                self.selected_index = _index
                break
        else:
            # didn't click any
            self.selected_index = -1

        self.update_obstacles_status()


    def check_point_inside_obstacle(self, point: tuple) -> bool:
        for _obs in self.get_obstacles():
            if _obs.check_point_inside(point):
                return True
            
        return False


    def update_obstacles_status(self):
        """Update the active status of each obstacle"""
        for index, obstacle in enumerate(self.__all_obstacles):
            if index == self.selected_index:
                obstacle.set_active(True)
            else:
                obstacle.set_active(False)    

obstacle_manager = ObstacleManager()