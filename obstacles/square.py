import math
import pygame
pygame.init()

class SquareObstacle():
    def __init__(self, center_pos: tuple, side_length: float, rotation_deg: float):
        self.x, self.y = center_pos
        self.side_length = side_length
        self.rotation_deg = rotation_deg
        self.rotation_rad = self.rotation_deg * math.pi/180

        self.selected = False
        
        self.__setup_points()

        # visualizing
        self.temp_draw_point = (0,0)

        self.closest_point = (0,0)
        self.second_closest_point = (0,0)

        self.find_normal_at_point((
            (self.points_xy[0][0] + (self.points_xy[1][0] * 2)) / 3,
            (self.points_xy[0][1] + (self.points_xy[1][1] * 2)) / 3))


    def __repr__(self) -> str:
        return f"Square Obstacle at pos: ({self.x}, {self.y}) rotation: {self.rotation_deg} side_length: {self.side_length}"


    def __vec(self, point1, point2) -> tuple:
        return ((point2[0] - point1[0]), (point2[1] - point1[1]))


    def __dot(self, vec1, vec2) -> float:
        return (vec1[0] * vec2[0] + vec1[1] * vec2[1])


    def __setup_points(self):
        self.points_xy = [(self.x - self.side_length, self.y - self.side_length),
                          (self.x - self.side_length, self.y + self.side_length),
                          (self.x + self.side_length, self.y + self.side_length),
                          (self.x + self.side_length, self.y - self.side_length)]

        rotation_matrix = [[math.cos(self.rotation_rad), -math.sin(self.rotation_rad)],
                           [math.sin(self.rotation_rad),  math.cos(self.rotation_rad)]]
        
        translated_points = [(p[0] - self.x, p[1] - self.y) for p in self.points_xy]

        rotated_points = [(rotation_matrix[0][0]*p[0] + rotation_matrix[0][1]*p[1], 
                           rotation_matrix[1][0]*p[0] + rotation_matrix[1][1]*p[1]) for p in translated_points]
        
        self.points_xy = [(p[0] + self.x, p[1] + self.y) for p in rotated_points]


    def move_by(self, amount: tuple) -> None:
        """Move the whole square in a direction"""
        self.x += amount[0]
        self.y += amount[1]

        self.__setup_points()


    def set_active(self, state: bool) -> None:
        """Sets selected state"""
        self.selected = state


    def find_normal_at_point(self, point: tuple) -> tuple:
        """Returns a vector containing the surface's normal from the point of impact"""
        distances = self.get_vertex_distances(point)
        s = set(distances)
        
        # used to convert any of the list/tuple to the distinct element and sorted sequence of elements
        min_dist, second_min_dist = sorted(s)[0], sorted(s)[1]

        self.closest_point = self.points_xy[distances.index(min_dist)]
        self.second_closest_point = self.points_xy[distances.index(second_min_dist)]

        point = self.get_closest_point(self.closest_point, self.second_closest_point, point)

        vec = (self.second_closest_point[0] - self.closest_point[0], self.second_closest_point[1] - self.closest_point[1])
        vec = (vec[1] + point[0], -vec[0] + point[1])

        # visualizing
        self.temp_draw_point = point
        self.normal = vec

        vec_mag = math.sqrt( math.pow(vec[0] - point[0], 2) + math.pow(vec[1] - point[1], 2))
        
        vec = ((vec[0] - point[0]) / vec_mag, 
               (vec[1] - point[1]) / vec_mag)

        return vec


    def get_vertex_distances(self, point: tuple) -> list:
        distances = [math.sqrt(math.pow((point[0] - self.points_xy[0][0]), 2) + math.pow((point[1] - self.points_xy[0][1]), 2)),
                     math.sqrt(math.pow((point[0] - self.points_xy[1][0]), 2) + math.pow((point[1] - self.points_xy[1][1]), 2)),
                     math.sqrt(math.pow((point[0] - self.points_xy[2][0]), 2) + math.pow((point[1] - self.points_xy[2][1]), 2)),
                     math.sqrt(math.pow((point[0] - self.points_xy[3][0]), 2) + math.pow((point[1] - self.points_xy[3][1]), 2))]

        return distances


    def get_closest_point(self, A, B, P) -> tuple:
        """Get closest point on the edge AB from point P"""
        a_to_p = [P[0] - A[0], P[1] - A[1]]     # Storing vector A->P
        a_to_b = [B[0] - A[0], B[1] - A[1]]     # Storing vector A->B

        atb2 = a_to_b[0]**2 + a_to_b[1]**2 # distance squared

        atp_dot_atb = a_to_p[0]*a_to_b[0] + a_to_p[1]*a_to_b[1] # The dot product of a_to_p and a_to_b

        t = atp_dot_atb / atb2              # The normalized distance from a to your closest point 

        return (A[0] + a_to_b[0]*t, A[1] + a_to_b[1]*t)


    def check_point_inside(self, point: tuple) -> bool:
        """Check if point is inside the sqare"""
        # TODO: Better performance can be achieved by removing function call overhead, just paste lines into here. Will look bad though
        AB = self.__vec(self.points_xy[0], self.points_xy[1])
        AM = self.__vec(self.points_xy[0], point)
        BC = self.__vec(self.points_xy[1], self.points_xy[2])
        BM = self.__vec(self.points_xy[1], point)

        dotABAM = self.__dot(AB, AM)
        dotABAB = self.__dot(AB, AB)
        dotBCBM = self.__dot(BC, BM)
        dotBCBC = self.__dot(BC, BC)

        return (0 <= dotABAM and dotABAM <= dotABAB and
                 0 <= dotBCBM and dotBCBM <= dotBCBC)


    def draw(self, screen: pygame.Surface):
        if self.selected:
            pygame.draw.lines(screen, (250,250,250), True, (self.points_xy[0],self.points_xy[1],self.points_xy[2],self.points_xy[3]))
        else:
            pygame.draw.lines(screen, (180,180,180), True, (self.points_xy[0],self.points_xy[1],self.points_xy[2],self.points_xy[3]))

        # DEBUGGING VISUALS
        # normal
        # pygame.draw.circle(screen, (200, 200, 200), self.temp_draw_point, 2)
        # pygame.draw.line(screen, (255,255,255), self.temp_draw_point, self.normal)

        # closest points
        # pygame.draw.circle(screen, (200, 0, 0), self.closest_point, 3)
        # pygame.draw.circle(screen, (200, 0, 0), self.second_closest_point, 3)

