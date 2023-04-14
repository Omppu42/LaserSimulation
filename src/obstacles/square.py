import math
import pygame
pygame.init()

from obstacles.obstacle import ObstacleSuper

class SquareObstacle(ObstacleSuper):
    def __init__(self, center_pos: tuple, side_length: float, rotation_deg: float):
        super().__init__(center_pos, side_length, rotation_deg)
        

    def __repr__(self) -> str:
        return f"Square Obstacle at pos: ({self.x}, {self.y}) rotation: {self.rotation_deg} side_length: {self.radius}"


    def __vec(self, point1, point2) -> tuple:
        return ((point2[0] - point1[0]), (point2[1] - point1[1]))


    def __get_closest_point(self, A, B, P) -> tuple:
        """Get closest point on the edge AB from point P"""
        a_to_p = [P[0] - A[0], P[1] - A[1]]     # Storing vector A->P
        a_to_b = [B[0] - A[0], B[1] - A[1]]     # Storing vector A->B

        atb2 = a_to_b[0]**2 + a_to_b[1]**2 # distance squared

        atp_dot_atb = a_to_p[0]*a_to_b[0] + a_to_p[1]*a_to_b[1] # The dot product of a_to_p and a_to_b

        t = atp_dot_atb / atb2              # The normalized distance from a to your closest point 

        return (A[0] + a_to_b[0]*t, A[1] + a_to_b[1]*t)
    

    def __get_vertex_distances(self, point: tuple) -> list:
        distances = [math.sqrt(math.pow((point[0] - self.points_xy[0][0]), 2) + math.pow((point[1] - self.points_xy[0][1]), 2)),
                     math.sqrt(math.pow((point[0] - self.points_xy[1][0]), 2) + math.pow((point[1] - self.points_xy[1][1]), 2)),
                     math.sqrt(math.pow((point[0] - self.points_xy[2][0]), 2) + math.pow((point[1] - self.points_xy[2][1]), 2)),
                     math.sqrt(math.pow((point[0] - self.points_xy[3][0]), 2) + math.pow((point[1] - self.points_xy[3][1]), 2))]

        return distances
    

    def update_drawing(self):
         # Convert the rotation angle from degrees to radians.
        self.rotation_rad = self.rotation_deg * math.pi/180
        
        # Define the points of the object as a list of tuples (x,y) based on its current position and radius.
        self.points_xy = [(self.x - self.radius, self.y - self.radius),
                        (self.x - self.radius, self.y + self.radius),
                        (self.x + self.radius, self.y + self.radius),
                        (self.x + self.radius, self.y - self.radius)]
        
        # Define the rotation matrix based on the current rotation angle.
        rotation_matrix = [[math.cos(self.rotation_rad), -math.sin(self.rotation_rad)],
                        [math.sin(self.rotation_rad),  math.cos(self.rotation_rad)]]
        
        # Translate the points of the object so that they are centered at the origin.
        translated_points = [(p[0] - self.x, p[1] - self.y) for p in self.points_xy]
        
        # Rotate the translated points using the rotation matrix.
        rotated_points = [(rotation_matrix[0][0]*p[0] + rotation_matrix[0][1]*p[1], 
                        rotation_matrix[1][0]*p[0] + rotation_matrix[1][1]*p[1]) for p in translated_points]
        
        # Translate the rotated points back to their original position.
        self.points_xy = [(p[0] + self.x, p[1] + self.y) for p in rotated_points]


    def find_normal_at_point(self, point: tuple) -> tuple:
        """Returns a vector containing the surface's normal from the point of impact"""
        distances = self.__get_vertex_distances(point)
        s = set(distances)
        s = sorted(s)

        # used to convert any of the list/tuple to the distinct element and sorted sequence of elements
        if len(s) == 1:
            return (0,0)
        else:
            min_dist, second_min_dist = s[0], s[1]

        self.closest_point = self.points_xy[distances.index(min_dist)]
        self.second_closest_point = self.points_xy[distances.index(second_min_dist)]

        point = self.__get_closest_point(self.closest_point, self.second_closest_point, point)

        vec = (self.second_closest_point[0] - self.closest_point[0], self.second_closest_point[1] - self.closest_point[1])
        vec = (vec[1] + point[0], -vec[0] + point[1])

        vec_mag = math.sqrt( math.pow(vec[0] - point[0], 2) + math.pow(vec[1] - point[1], 2))
        
        vec = ((vec[0] - point[0]) / vec_mag, 
               (vec[1] - point[1]) / vec_mag)

        return vec


    def check_point_inside(self, point: tuple) -> bool:
        """Check if point is inside the sqare"""
        AB = self.__vec(self.points_xy[0], self.points_xy[1])
        AM = self.__vec(self.points_xy[0], point)
        BC = self.__vec(self.points_xy[1], self.points_xy[2])
        BM = self.__vec(self.points_xy[1], point)

        dotABAM = (AB[0] * AM[0] + AB[1] * AM[1])
        dotABAB = (AB[0] * AB[0] + AB[1] * AB[1])
        dotBCBM = (BC[0] * BM[0] + BC[1] * BM[1])
        dotBCBC = (BC[0] * BC[0] + BC[1] * BC[1])

        return (0 <= dotABAM and dotABAM <= dotABAB and
                 0 <= dotBCBM and dotBCBM <= dotBCBC)


    def draw(self, screen: pygame.Surface):
        if self.selected:
            pygame.draw.lines(screen, (250,250,250), True, (self.points_xy[0],self.points_xy[1],self.points_xy[2],self.points_xy[3]))
        else:
            pygame.draw.lines(screen, (180,180,180), True, (self.points_xy[0],self.points_xy[1],self.points_xy[2],self.points_xy[3]))

    
    def make_json_save(self) -> dict:
        out = {}
        out["position"] = {"x": self.x, "y": self.y}
        out["rotation"] = self.rotation_deg
        out["scale"] = self.radius
        
        return out
    

    def load_from_json(self, dict) -> None:
        square_part = dict["squares"]

        self.x = square_part["position"]["x"]
        self.y = square_part["position"]["y"]

        self.radius = square_part["scale"]
        self.rotation_deg = square_part["rotation"]

        self.update_drawing()