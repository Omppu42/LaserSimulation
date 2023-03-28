import math
import pygame
pygame.init()

class SquareObstacle():
    def __init__(self, center_pos: tuple, side_length: float, rotation_deg: float):
        self.center_pos = center_pos
        self.side_length = side_length
        self.rotation_deg = rotation_deg
        self.rotation_rad = self.rotation_deg * math.pi/180

        self.selected = False

        # self.surf = pygame.Surface((side_length, side_length), pygame.SRCALPHA)
        # self.surf.fill((100,100,100))
        # self.surf = pygame.transform.rotate(self.surf, -self.rotation_deg)
        # self.rect = self.surf.get_rect(center=(self.center_pos))

        self.points_xy = [(center_pos[0] - side_length, center_pos[1] - side_length),
                          (center_pos[0] - side_length, center_pos[1] + side_length),
                          (center_pos[0] + side_length, center_pos[1] + side_length),
                          (center_pos[0] + side_length, center_pos[1] - side_length)]
        
        self.__rotate_points()

        # print("Center:", center_pos, "Side length:", side_length)
        # print(self.points_xy)
        self.temp_draw_point = (0,0)
        self.closest_point = (0,0)
        self.second_closest_point = (0,0)

        self.find_normal_at_point((
            (self.points_xy[0][0] + (self.points_xy[1][0] * 2)) / 3,
            (self.points_xy[0][1] + (self.points_xy[1][1] * 2)) / 3))


    def __repr__(self) -> str:
        return f"Square Obstacle at pos: {self.center_pos} rotation: {self.rotation_deg} side_length: {self.side_length}"


    def __vec(self, point1, point2) -> tuple:
        return ((point2[0] - point1[0]), (point2[1] - point1[1]))


    def __dot(self, vec1, vec2) -> float:
        return (vec1[0] * vec2[0] + vec1[1] * vec2[1])


    def __rotate_points(self):
        rotation_matrix = [[math.cos(self.rotation_rad), -math.sin(self.rotation_rad)],
                           [math.sin(self.rotation_rad),  math.cos(self.rotation_rad)]]
        
        translated_points = [(p[0] - self.center_pos[0], p[1] - self.center_pos[1]) for p in self.points_xy]

        rotated_points = [(rotation_matrix[0][0]*p[0] + rotation_matrix[0][1]*p[1], 
                           rotation_matrix[1][0]*p[0] + rotation_matrix[1][1]*p[1]) for p in translated_points]
        
        self.points_xy = [(p[0] + self.center_pos[0], p[1] + self.center_pos[1]) for p in rotated_points]


    def set_active(self, state: bool) -> None:
        """Sets selected state"""
        self.selected = state


    def find_normal_at_point(self, point: tuple) -> tuple:
        """Returns a vector containing the surface's normal from the point of impact"""

        self.temp_draw_point = point
        distances = self.get_vertex_distances(point)

        s = set(distances)
        
        # used to convert any of the list/tuple to the distinct element and sorted sequence of elements
        min_dist, second_min_dist = sorted(s)[0], sorted(s)[1]

        lowers_point = self.points_xy[distances.index(min_dist)]
        second_lowers_point = self.points_xy[distances.index(second_min_dist)]

        self.closest_point = lowers_point
        self.second_closest_point = second_lowers_point

        vec = (second_lowers_point[0] - lowers_point[0], second_lowers_point[1] - lowers_point[1])
        vec = (vec[1] + point[0], -vec[0] + point[1])

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



    def check_clicked(self, point) -> bool:
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

        # normal
        # pygame.draw.circle(screen, (200, 200, 200), self.temp_draw_point, 2)
        # pygame.draw.line(screen, (255,255,255), self.temp_draw_point, self.normal)

        # closest points
        # pygame.draw.circle(screen, (200, 0, 0), self.closest_point, 3)
        # pygame.draw.circle(screen, (200, 0, 0), self.second_closest_point, 3)


    def check_point_on_edge(self, point: tuple, points_to_discard: tuple) -> tuple:
        """Takes point to check collision with and points that were hit last time.\n 
        Return two points from self.points_xy if hit between them"""
        for _i in range(4):
            sec_index = (_i + 1) % 4

            if not points_to_discard == None: 
                if self.points_xy[_i] == points_to_discard[0] and self.points_xy[sec_index] == points_to_discard[1]: continue

            
            dist_to_first =          math.sqrt(math.pow(point[0] - self.points_xy[_i][0], 2)                  + math.pow(point[1] - self.points_xy[_i][1], 2))
            dist_to_second =         math.sqrt(math.pow(point[0] - self.points_xy[sec_index][0], 2)              + math.pow(point[1] - self.points_xy[sec_index][1], 2))
            dist_between_verticies = math.sqrt(math.pow(self.points_xy[_i][0] - self.points_xy[sec_index][0], 2) + math.pow(self.points_xy[_i][1] - self.points_xy[sec_index][1], 2))

            # hit corner
            #if dist_to_first < 1 + 10 / self.side_length: 
            if dist_to_first < 2: 
                distances = self.get_vertex_distances(point)
                s = set(distances)
                
                # used to convert any of the list/tuple to the distinct element and sorted sequence of elements
                second_min_dist = sorted(s)[1]
                return (self.points_xy[_i], self.points_xy[distances.index(second_min_dist)])

            # hit edge
            diff = abs(dist_between_verticies - (dist_to_first + dist_to_second))

            if diff < 0.05:
                return (self.points_xy[_i], self.points_xy[sec_index])
            
        return None
    

class CircleObstacle():
    def __init__(self, center_pos: tuple, radius: float):
        self.x, self.y = center_pos
        self.radius = radius
        self.surf = pygame.Surface((2 * self.radius, 2 * self.radius), pygame.SRCALPHA, 32)
        self.surf = self.surf.convert_alpha()
        self.surf.fill((0, 0, 0, 0))
        
        self.width = 1
        self.selected = False

        self.redraw_surf()

        self.rect = self.surf.get_rect(center=(self.x, self.y))

    
    def __repr__(self) -> str:
        return f"Circle Obstacle at pos: ({self.x}, {self.y}) radius: {self.radius}"


    def set_active(self, state: bool) -> None:
        """Sets selected state"""
        self.selected = state
        self.redraw_surf()

    def redraw_surf(self) -> None:
        col = (250, 250, 250, 255) if self.selected else (180, 180, 180, 255)
        pygame.draw.circle(self.surf, col, (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.surf, (0, 0, 0, 0), (self.radius, self.radius), self.radius - self.width)


    def draw(self, screen: pygame.Surface):
        screen.blit(self.surf, self.rect)


    def check_clicked(self, point) -> bool:
        dist_to_center = math.sqrt( math.pow(self.x - point[0], 2) + math.pow(self.y - point[1], 2) )
        return dist_to_center < self.radius
    

    def check_collision(self, point: tuple, circle_last_hit_cetnerxy: tuple) -> tuple | None:
        """If point inside circle, return tuple of circle's center x and y. Else return None"""
        if circle_last_hit_cetnerxy == (self.x, self.y): return None
        
        dist_to_center = math.sqrt( math.pow(self.x - point[0], 2) + math.pow(self.y - point[1], 2) )

        if self.radius <= 30:
            if dist_to_center < self.radius:
                return (self.x, self.y)

        elif self.radius > 30:
            if dist_to_center < self.radius and dist_to_center > self.radius - self.width:
                return (self.x, self.y)
        
        return None
            
    
    def find_normal_at_point(self, point: tuple) -> tuple:
        normal = (point[0] - self.x, point[1] - self.y)

        length = math.sqrt( math.pow(normal[0], 2) + math.pow(normal[1], 2) )
        normal = (normal[0] / length, normal[1] / length)

        return normal