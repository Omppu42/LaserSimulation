import pygame
pygame.init()

from obstacles.square import SquareObstacle
from obstacles.circle import CircleObstacle

from config.stats import stats

class ObstacleManager():
    def __init__(self) -> None:
        self.__obstacles_square = [ SquareObstacle((300, 300), 100, 30), SquareObstacle((600, 150), 100, 60), 
                                    SquareObstacle((600, 300), 50, 85), SquareObstacle((500, 480), 40, 20),
                                    SquareObstacle((250, 525), 100, 82), SquareObstacle((475, 675), 100, 70), SquareObstacle((600, 480), 100, 70)]

        self.__obstacles_circle = [CircleObstacle(( 440, 250), 50), CircleObstacle(( 450, 180), 50), CircleObstacle(( 400, 500), 20), CircleObstacle(( 600, 360), 20)]
        
        self.__obstacles_square.sort(key=lambda x: x.side_length)
        self.__obstacles_circle.sort(key=lambda x: x.radius)

        self.__all_obstacles = self.__obstacles_circle + self.__obstacles_square
        self.selected_index = -1


    def get_obstacles(self) -> list:
        return self.__all_obstacles
    

    def get_selected_obstacle(self) -> SquareObstacle | CircleObstacle:
        return self.__all_obstacles[self.selected_index]
    

    def draw_obstacles(self, screen) -> None:
        for obs in self.__all_obstacles:
            obs.draw(screen)


    def handle_events(self, event) -> None:
        stats.total_obstacles = len(self.__all_obstacles)

        if self.selected_index == -1: return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
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
            
                    
    
    def mouse_motion(self) -> None:
        if stats.simulation_running: return
        
        if pygame.mouse.get_pressed()[0]:
            if self.selected_index != -1:
                mouse_moved = pygame.mouse.get_rel()

                _selected_obs = obstacle_manager.get_obstacles()[self.selected_index]
                _selected_obs.move_by(mouse_moved)


    def check_mouse_up(self) -> None:
        self.selected_index = -1
        self.update_obstacle_status()


    def check_click(self, mouse_pos: tuple) -> None:
        if stats.simulation_running: return

        pygame.mouse.get_rel()

        for index, ostacle in enumerate(obstacle_manager.get_obstacles()):
            # already selected
            if index == self.selected_index: continue

            # check if clicked
            if ostacle.check_point_inside(mouse_pos):
                self.selected_index = obstacle_manager.get_obstacles().index(ostacle)
                break
        else:
            # didn't click any
            self.selected_index = -1

        self.update_obstacle_status()


    def update_obstacle_status(self):
        # update selected status
        for index, obstacle in enumerate(self.__all_obstacles):
            if index == self.selected_index:
                obstacle.set_active(True)
            else:
                obstacle.set_active(False)    

obstacle_manager = ObstacleManager()