from square import SquareObstacle
from circle import CircleObstacle

class ObstacleManager():
    def __init__(self) -> None:
        self.__obstacles_square = [ SquareObstacle((300, 300), 100, 30), SquareObstacle((600, 150), 100, 60), 
                                    SquareObstacle((600, 300), 50, 85), SquareObstacle((500, 480), 40, 20),
                                    SquareObstacle((250, 525), 100, 82), SquareObstacle((475, 675), 100, 70), SquareObstacle((600, 480), 100, 70)]

        self.__obstacles_circle = [CircleObstacle(( 440, 250), 50), CircleObstacle(( 450, 180), 50), CircleObstacle(( 400, 500), 20), CircleObstacle(( 600, 360), 20)]
        
        self.__obstacles_square.sort(key=lambda x: x.side_length)
        self.__obstacles_circle.sort(key=lambda x: x.radius)

        self.__all_obstacles = self.__obstacles_circle + self.__obstacles_square

    def get_obstacles(self) -> list:
        return self.__all_obstacles
    

    def draw_obstacles(self, screen) -> None:
        for obs in self.__all_obstacles:
            obs.draw(screen)


obstacle_manager = ObstacleManager()